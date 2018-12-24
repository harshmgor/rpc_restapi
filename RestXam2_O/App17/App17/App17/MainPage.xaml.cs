using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;
using System.Collections.Concurrent;
using Newtonsoft.Json;
using System.Collections.ObjectModel;

namespace App17
{
    public class Meta
    {
        public int limit { get; set; }
        public object next { get; set; }
        public int offset { get; set; }
        public object previous { get; set; }
        public int total_count { get; set; }
    }

    public class Object
    {
        public string body { get; set; }
        public DateTime created_at { get; set; }
        public int id { get; set; }
        public string resource_uri { get; set; }
        public string title { get; set; }
    }

    public class RootObject
    {
        public Meta meta { get; set; }
        public List<Object> objects { get; set; }
    }
    public class RpcClient
    {
        private readonly IConnection connection;
        private readonly IModel channel;
        private readonly string replyQueueName;
        private readonly EventingBasicConsumer consumer;
        private readonly BlockingCollection<string> respQueue = new BlockingCollection<string>();
        private readonly IBasicProperties props;

        public RpcClient()
        {
            ConnectionFactory factory = new ConnectionFactory();
            factory.Uri = new Uri("amqp://udpbbklh:Ttvn6qar8lu2aLE-ie3CmvdZ1ReLLg3k@bee.rmq.cloudamqp.com/udpbbklh");

            connection = factory.CreateConnection();
            channel = connection.CreateModel();
            replyQueueName = channel.QueueDeclare().QueueName;
            consumer = new EventingBasicConsumer(channel);

            props = channel.CreateBasicProperties();
            var correlationId = Guid.NewGuid().ToString();
            props.CorrelationId = correlationId;
            props.ReplyTo = replyQueueName;

            consumer.Received += (model, ea) =>
            {
                var body = ea.Body;
                var response = Encoding.UTF8.GetString(body);
                if (ea.BasicProperties.CorrelationId == correlationId)
                {
                    respQueue.Add(response);
                }
            };
        }

        public string Call(string message)
        {

            var messageBytes = Encoding.UTF8.GetBytes(message);
            channel.BasicPublish(
                exchange: "",
                routingKey: "rpc_queue",
                basicProperties: props,
                body: messageBytes);

            channel.BasicConsume(
                consumer: consumer,
                queue: replyQueueName,
                autoAck: true);

            return respQueue.Take(); ;
        }

        public void Close()
        {
            connection.Close();
        }
    }
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();
        }
        protected override async void OnAppearing() {

            var rpcClient = new RpcClient();
            string sms = "get/";
            var response = rpcClient.Call(sms);

            var post = JsonConvert.DeserializeObject<List<Object>>(response);
            //ObservableCollection<Object> _post = new ObservableCollection<Object>(post.objects as List<Object>);
            Post_List.ItemsSource = post;
            base.OnAppearing();
            await DisplayAlert("alert", "sent", "ok");
        }
        private async void onAdd(object sender, System.EventArgs e) {
            var rpcClient = new RpcClient();
            string sms = "post/" + "title/" + EntTitle.Text + "/" + "body/"+ EntBody.Text + "/";
            var response = rpcClient.Call(sms);
            await DisplayAlert("alert", "sent", "ok");
        }
        private async void onPut(object sender,System.EventArgs e) {
            var rpcClient = new RpcClient();
            //rpc_client.py put/74/title/title/body/body/
            var sms = "put/" + Convert.ToInt32(EntId.Text) + "/" + "title/" + EntBody.Text + "/" + "body/" + EntBody.Text + "/";
            var response = rpcClient.Call(sms);
            await DisplayAlert("alert", "sent", "ok");
        }
        private async void onDelete(object sender,System.EventArgs e) {
            var rpcClient = new RpcClient();
            var sms = "delete/" + Convert.ToInt32(EntId.Text) + "/";
            var response = rpcClient.Call(sms);
            await DisplayAlert("alert", "sent", "ok");
        }
    }
}
