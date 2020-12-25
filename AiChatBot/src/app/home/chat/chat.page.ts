import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { IonContent } from '@ionic/angular';
import { ChatService } from 'src/app/services/chat.service';
import { message } from '../../models/message.model';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.page.html',
  styleUrls: ['./chat.page.scss'],
})
export class ChatPage implements OnInit {
  newMsg = '';
  UserMsg : message;
  @ViewChild(IonContent) content : IonContent;
  constructor(private chatApi : ChatService, route : ActivatedRoute) { 
    route.params.subscribe(() => {
      this.ngOnInit();
    });

  }

  messages =[
  //   {
  //   user:'vineeth',
  //   msg:'Hello there!',
  //   createdAt : 1
  // },
  // {
  //   user:'Ai',
  //   msg:'Hi',
  //   createdAt : 2
  // },
  // {
  //   user:'vineeth',
  //   msg:'How are you?',
  //   createdAt : 3
  // },
  // {
  //   user:'Ai',
  //   msg:'Great',
  //   createdAt : 4
  // }
];
currentUser="You";
sendMessage(){
  this.UserMsg = new message(this.newMsg);
  this.messages.push({user:"You",msg: this.newMsg, createdAt: new Date().getTime()});
  this.scroll();
  this.chatApi.sendMessage(this.UserMsg).subscribe(response =>{
    setTimeout(() =>{
      this.messages.push({user:"Simba",msg: response.message, createdAt: new Date().getTime()});
      this.scroll();
  },250);
  });
  this.newMsg='';
  
}
  scroll(){
    setTimeout(() =>{
      this.content.scrollToBottom(250);
    },100);
  }
  ngOnInit() {
    this.messages=this.chatApi.messages;
    setTimeout(() =>{
      this.content.scrollToBottom(0);
    });
  }

}
