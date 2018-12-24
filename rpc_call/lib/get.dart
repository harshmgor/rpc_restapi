import 'package:flutter/material.dart';
import 'rpc_client.dart';
import 'dart:convert';
import 'dart:core';

class getData extends StatefulWidget {
  @override
  getDataState createState() => getDataState();
}

class getDataState extends State<getData> {
  List data;

  Future<String> getData() async {
    RpcClient client = new RpcClient();
    client.call("get/").then((var val) {
      print(json.decode(val));
      setState((){
        data=json.decode(val)['objects'];
      });

    }).then((_) => client.close());
    return "Success";
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      body: ListView.builder(
        itemCount: data == null ? 0 : data.length,
        itemBuilder: (BuildContext context, int index) {
          return new Container(
            child: Center(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  Card(
                    child: Container(
                        padding: EdgeInsets.all(15.0),
                        child: Row(
                          children: <Widget>[
                            Text("ID: "),
                            Text(data[index]["id"].toString(),
                                style: TextStyle(
                                    fontSize: 18.0, color: Colors.black87)),
                          ],
                        )),
                  ),
                  Card(
                    child: Container(
                        padding: EdgeInsets.all(15.0),
                        child: Row(
                          children: <Widget>[
                            Text("Title: "),
                            Text(data[index]["title"].toString(),
                                style: TextStyle(
                                    fontSize: 18.0, color: Colors.black87)),
                          ],
                        )),
                  ),
                  Card(
                    child: Container(
                        padding: EdgeInsets.all(15.0),
                        child: Row(
                          children: <Widget>[
                            Text("Body: "),
                            Text(data[index]["body"].toString(),
                                style: TextStyle(
                                    fontSize: 18.0, color: Colors.red)),
                          ],
                        )),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    this.getData();
  }
}
