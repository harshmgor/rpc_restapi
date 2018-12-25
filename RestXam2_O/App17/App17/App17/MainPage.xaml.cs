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
    //creating classes for binding response data Meta,Object,RootObject
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
    //rpc client class starts here
    public class RpcClient
    {
        //initilising readonly variables for later uses
        private readonly IConnection connection;
        private readonly IModel channel;
        private readonly string replyQueueName;
        private readonly EventingBasicConsumer consumer;
        private readonly BlockingCollection<string> respQueue = new BlockingCollection<string>();
        private readonly IBasicProperties props;

        public RpcClient()
        {
            //establising connction with my rabbitmq message brocker
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
        //handles the request // CURD method name and user params  
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
        
            //initilising instance of rpcClient
            var rpcClient = new RpcClient();
            //setting my request method to get
            string sms = "get/";
            //passing the value to rpcClient.call()
            var response = rpcClient.Call(sms);

            //handling the response
            //decerializing json responce to object
            var post = JsonConvert.DeserializeObject<List<Object>>(response);
            //binding the json object with listview item fields id,title,body
            Post_List.ItemsSource = post;
            //load the data when app starts
            base.OnAppearing();
        }
        //button event for post method
        private async void onAdd(object sender, System.EventArgs e) {
            var rpcClient = new RpcClient();
            //setting the values to be passed to call method
            string sms = "post/" + "title/" + EntTitle.Text + "/" + "body/"+ EntBody.Text + "/";
            //calling the method for post request
            var response = rpcClient.Call(sms);
            await DisplayAlert("alert", "post request sent", "ok");
        }
        private async void onPut(object sender,System.EventArgs e) {
            var rpcClient = new RpcClient();
            //setting the values to be passed to call method
            var sms = "put/" + Convert.ToInt32(EntId.Text) + "/" + "title/" + EntBody.Text + "/" + "body/" + EntBody.Text + "/";
            var response = rpcClient.Call(sms);
            await DisplayAlert("alert", "put request sent", "ok");
        }
        private async void onDelete(object sender,System.EventArgs e) {
            var rpcClient = new RpcClient();
            //setting the values to be passed to call method
            var sms = "delete/" + Convert.ToInt32(EntId.Text) + "/";
            var response = rpcClient.Call(sms);
            await DisplayAlert("alert", "delete sent", "ok");
        }
    }
}
