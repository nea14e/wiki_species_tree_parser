import {Component, inject, input, output} from '@angular/core';
import {RootDataKeeperService} from '../root-data-keeper.service';
import {Item} from '../../models/item';
import {Level} from '../../models/level';

@Component({
  selector: 'app-plain-list-item',
  imports: [],
  templateUrl: './plain-list-item.html',
  styleUrl: './plain-list-item.css',
})
export class PlainListItemComponent {
  public rootData = inject(RootDataKeeperService);

  level = input<Level | null>(null);
  item = input<Item | null>(null);
  isShowTreeRootIcon = input(false);
  isShowDeleteButton = input(false);
  deleteButtonDescription = input<string | null>(null);

  click = output<void>();
  delete = output<void>();
}
