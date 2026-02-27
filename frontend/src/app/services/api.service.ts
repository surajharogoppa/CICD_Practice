import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getInfo(): Observable<any> {
    return this.http.get<any>(`${this.base}/api/info`);
  }

  getJoke(): Observable<any> {
    return this.http.get<any>(`${this.base}/api/joke`);
  }

  getQuote(): Observable<any> {
    return this.http.get<any>(`${this.base}/api/quote`);
  }

  coinFlip(): Observable<any> {
    return this.http.get<any>(`${this.base}/api/coinflip`);
  }

  rollDice(sides: number, count: number): Observable<any> {
    return this.http.get<any>(`${this.base}/api/dice?sides=${sides}&count=${count}`);
  }

  register(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.base}/api/users/register`, { username, password });
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.base}/api/users/login`, { username, password });
  }

  getMessages(): Observable<any> {
    return this.http.get<any>(`${this.base}/api/messages`);
  }

  postMessage(username: string, text: string): Observable<any> {
    return this.http.post<any>(`${this.base}/api/messages`, { username, text });
  }

  reverseText(text: string): Observable<any> {
    return this.http.post<any>(`${this.base}/api/utils/reverse`, { text });
  }

  wordCount(text: string): Observable<any> {
    return this.http.post<any>(`${this.base}/api/utils/wordcount`, { text });
  }
}
