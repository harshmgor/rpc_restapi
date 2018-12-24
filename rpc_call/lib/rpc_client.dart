import 'package:dart_amqp/dart_amqp.dart';
import 'dart:io';
import 'dart:async';

class RpcClient {
  int _nextCorrelationId = 1;
  final Completer connected = new Completer();
  final Client client;
  final Map<String, Completer> _pendingOperations =
      new Map<String, Completer>();
  Queue _serverQueue;
  String _replyQueueName;

  static ConnectionSettings settings = new ConnectionSettings(
      host : "server",
      //port: 15672,
      virtualHost: "host-name",
      authProvider : new PlainAuthenticator("username", "password")
  );

  RpcClient() : client = new Client(settings : settings) {
    client
        .channel()
        .then((Channel channel) => channel.queue("rpc_queue"))
        .then((Queue rpcQueue) {
          _serverQueue = rpcQueue;

          // Allocate a private queue for server responses
          return rpcQueue.channel.privateQueue();
        })
        .then((Queue queue) => queue.consume())
        .then((Consumer consumer) {
          _replyQueueName = consumer.queue.name;
          consumer.listen(handleResponse);
          connected.complete();
        });
  }

  void handleResponse(AmqpMessage message) {
    // Ignore if the correlation id is unknown
    if (!_pendingOperations.containsKey(message.properties.corellationId)) {
      return;
    }

    _pendingOperations
        .remove(message.properties.corellationId)
        .complete(message.payloadAsString);
  }

  Future call(var data) {
    // Make sure we are connected before sending the request
    return connected.future.then((_) {
      String uuid = "${_nextCorrelationId++}";
      Completer completer = new Completer();

      MessageProperties properties = new MessageProperties()
        ..replyTo = _replyQueueName
        ..corellationId = uuid;

      _pendingOperations[uuid] = completer;

      _serverQueue.publish(data, properties: properties);

      return completer.future;
    });
  }

  Future close() {
    // Kill any pending responses
    _pendingOperations.forEach((_, Completer completer) =>
        completer.completeError("RPC client shutting down"));
    _pendingOperations.clear();

    return client.close();
  }
}
