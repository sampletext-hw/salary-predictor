import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  @ViewChild("start") startRef!: ElementRef;

  constructor(
    private router: Router
  ) {
  }

  ngOnInit(): void {
  }

  goToNext() {
    this.startRef.nativeElement.classList.add('animate-scale')
    setTimeout(() => {
      this.router.navigate(['predict'])
    }, 200)
  }

}
