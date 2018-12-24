import 'package:flutter/material.dart';
import './get.dart' as api_get;
import './post.dart' as api_post;
import './update.dart' as api_update;

void main(){
  runApp(MaterialApp(
    home: tabs(),
  ));
}

class tabs extends StatefulWidget {
  @override
  tabsState createState() => tabsState();
}

class tabsState extends State<tabs> with SingleTickerProviderStateMixin{
  TabController controller;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    controller = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    // TODO: implement dispose
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        title: Text("Rpc Calls"),
        backgroundColor: Colors.blueAccent,
        bottom: TabBar(
          controller: controller,
          tabs: <Widget>[
            Tab(text: "Get",),
            Tab(text: "Post",),
            Tab(text: "Put/Delete",)
          ],
        ),
      ),
      body: TabBarView(
        controller: controller,
        children: <Widget>[
          api_get.getData(),
          api_post.api_post(),
          api_update.api_update(),
        ],
      ),
    );
  }
}