import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:convert';
import 'rpc_client.dart';

class api_update extends StatelessWidget {
  final formkey = GlobalKey<FormState>();
  String txtTitle, txtBody, txtId;

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return new Card(
      child: Padding(
        padding: EdgeInsets.all(8.0),
        child: Form(
          key: formkey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              TextFormField(
                decoration: InputDecoration(
                  labelText: 'Id',
                ),
                onSaved: (input) => txtId = input,
                validator: (input) => input.length < 1 ? 'Empty' : null,
              ),
              TextFormField(
                decoration: InputDecoration(
                  labelText: 'Title',
                ),
                onSaved: (input) => txtTitle = input,
              ),
              TextFormField(
                decoration: InputDecoration(
                  labelText: 'Body',
                ),
                onSaved: (input) => txtBody = input,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: RaisedButton(
                      onPressed: submit,
                      child: Text('Send Data'),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: RaisedButton(
                      onPressed: delReq,
                      child: Text('Delete Data'),
                    ),
                  )
                ],
              )
            ],
          ),
        ),
      ),
    );
  }

  void submit() async{
    if(formkey.currentState.validate()){
      formkey.currentState.save();
      print(txtId);
      print(txtTitle);
      print(txtBody);

      var data="put/"+txtId.toString()+"/title/"+txtTitle.toString()+"/body/"+txtBody.toString()+"/";
      RpcClient client = new RpcClient();
      print(data);
      print(client.call(data)
         // .then((_) => client.close())
      );
    }
  }

  void delReq() async{

    if(formkey.currentState.validate()){
      formkey.currentState.save();
      print(txtId);
      print(txtTitle);
      print(txtBody);

      var data="delete/"+txtId.toString()+"/";
      RpcClient client = new RpcClient();
      print(data);
      print(client.call(data)
          //.then((_) => client.close())
      );
    }
  }

}