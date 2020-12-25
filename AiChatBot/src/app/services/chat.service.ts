import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { message } from '../models/message.model';

@Injectable({
  providedIn: 'root'
})
export class ChatService {  
  messages=[];
  baseurl="http://192.168.0.103:8000";
  httpHeaders = new HttpHeaders({'Content-Type' : 'application/json'});
  constructor(private http : HttpClient) { }
  sendMessage(msg : message):Observable<any>{
    return this.http.post(this.baseurl + "/chat/",msg);
  }
}
