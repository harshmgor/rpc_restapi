import 'package:flutter/material.dart';
import 'rpc_client.dart';

class api_post extends StatelessWidget {
  final formkey = GlobalKey<FormState>();
  String txtTitle, txtBody;

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
                  labelText: 'Title',
                ),
                onSaved: (input) => txtTitle = input,
                validator: (input) => input.length < 1 ? 'Empty' : null,
              ),
              TextFormField(
                decoration: InputDecoration(
                  labelText: 'Body',
                ),
                onSaved: (input) => txtBody = input,
                validator: (input) => input.length < 1 ? 'Empty' : null,
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
      print(txtTitle);
      print(txtBody);
      var data="post/title/"+txtTitle+"/body/"+txtBody+"/";
      RpcClient client = new RpcClient();
      print(data);
      print(client.call(data)
         // .then((_) => client.close())
      );

    }
  }

}

