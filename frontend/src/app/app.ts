import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {

  // Stats
  stats: any = { total_visits: 0, time: '', status: '' };

  // Joke
  joke: any = null;
  jokeLoading = false;

  // Quote
  quote: any = null;
  quoteLoading = false;

  // Coin
  coinResult = '';
  coinLoading = false;

  // Dice
  diceSides = 6;
  diceCount = 1;
  diceResult: any = null;
  diceLoading = false;

  // Register
  regUsername = '';
  regPassword = '';
  regMessage = '';
  regError = '';
  regLoading = false;

  // Login
  loginUsername = '';
  loginPassword = '';
  loginMessage = '';
  loginError = '';
  loginLoading = false;

  // Messages
  messages: any[] = [];
  msgUsername = '';
  msgText = '';
  msgResult = '';
  msgError = '';
  msgLoading = false;

  // Reverse
  reverseInput = '';
  reverseResult = '';
  reverseLoading = false;

  // Word Count
  wcInput = '';
  wcResult: any = null;
  wcLoading = false;

  constructor(private api: ApiService, private cd: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadStats();
    this.loadMessages();
  }

  loadStats(): void {
    this.api.getInfo().subscribe({
      next: (data: any) => {
        this.stats = data;
        this.cd.detectChanges();
      },
      error: () => { this.cd.detectChanges(); }
    });
  }

  getJoke(): void {
    this.jokeLoading = true;
    this.joke = null;
    this.api.getJoke().subscribe({
      next: (data: any) => {
        this.joke = data;
        this.jokeLoading = false;
        this.cd.detectChanges();
      },
      error: () => {
        this.jokeLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  getQuote(): void {
    this.quoteLoading = true;
    this.quote = null;
    this.api.getQuote().subscribe({
      next: (data: any) => {
        this.quote = data;
        this.quoteLoading = false;
        this.cd.detectChanges();
      },
      error: () => {
        this.quoteLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  coinFlip(): void {
    this.coinLoading = true;
    this.coinResult = '';
    this.api.coinFlip().subscribe({
      next: (data: any) => {
        this.coinResult = data.result;
        this.coinLoading = false;
        this.cd.detectChanges();
      },
      error: () => {
        this.coinLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  rollDice(): void {
    this.diceLoading = true;
    this.diceResult = null;
    this.api.rollDice(this.diceSides, this.diceCount).subscribe({
      next: (data: any) => {
        this.diceResult = data;
        this.diceLoading = false;
        this.cd.detectChanges();
      },
      error: () => {
        this.diceLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  register(): void {
    this.regMessage = ''; this.regError = ''; this.regLoading = true;
    this.api.register(this.regUsername, this.regPassword).subscribe({
      next: (data: any) => {
        this.regMessage = data.message;
        this.regLoading = false;
        this.cd.detectChanges();
        this.loadStats();
      },
      error: (err: any) => {
        this.regError = err.error?.error || 'Something went wrong';
        this.regLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  login(): void {
    this.loginMessage = ''; this.loginError = ''; this.loginLoading = true;
    this.api.login(this.loginUsername, this.loginPassword).subscribe({
      next: (data: any) => {
        this.loginMessage = data.message;
        this.loginLoading = false;
        this.cd.detectChanges();
      },
      error: (err: any) => {
        this.loginError = err.error?.error || 'Something went wrong';
        this.loginLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  loadMessages(): void {
    this.api.getMessages().subscribe({
      next: (data: any) => {
        this.messages = data.messages.reverse();
        this.cd.detectChanges();
      },
      error: () => { this.cd.detectChanges(); }
    });
  }

  postMessage(): void {
    this.msgResult = ''; this.msgError = ''; this.msgLoading = true;
    this.api.postMessage(this.msgUsername, this.msgText).subscribe({
      next: (data: any) => {
        this.msgResult = data.message;
        this.msgText = '';
        this.msgLoading = false;
        this.cd.detectChanges();
        this.loadMessages();
        this.loadStats();
      },
      error: (err: any) => {
        this.msgError = err.error?.error || 'Something went wrong';
        this.msgLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  reverseText(): void {
    this.reverseLoading = true;
    this.reverseResult = '';
    this.api.reverseText(this.reverseInput).subscribe({
      next: (data: any) => {
        this.reverseResult = data.reversed;
        this.reverseLoading = false;
        this.cd.detectChanges();
      },
      error: () => {
        this.reverseLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  wordCount(): void {
    this.wcLoading = true;
    this.wcResult = null;
    this.api.wordCount(this.wcInput).subscribe({
      next: (data: any) => {
        this.wcResult = data;
        this.wcLoading = false;
        this.cd.detectChanges();
      },
      error: () => {
        this.wcLoading = false;
        this.cd.detectChanges();
      }
    });
  }
}