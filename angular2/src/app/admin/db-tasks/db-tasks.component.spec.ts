import {ComponentFixture, TestBed} from '@angular/core/testing';

import {DbTasksComponent} from './db-tasks.component';

describe('AdminTasksComponent', () => {
  let component: DbTasksComponent;
  let fixture: ComponentFixture<DbTasksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DbTasksComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DbTasksComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
