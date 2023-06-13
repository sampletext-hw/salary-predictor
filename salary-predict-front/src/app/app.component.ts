import {Component, ElementRef, ViewChild} from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'salary-predict-front';

  @ViewChild("start") startRef!: ElementRef;

  constructor(
    private router: Router
  ) {
  }
}
