import {Component, OnInit} from '@angular/core';
import {NetworkService} from './network.service';
import {Tree} from './models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  tree: Tree;

  constructor(private networkService: NetworkService) {}

  ngOnInit(): void {
    this.networkService.getTreeDefault().subscribe(data => {
      this.tree = data;
    }, error => {
      alert(error);
    });
  }

}
