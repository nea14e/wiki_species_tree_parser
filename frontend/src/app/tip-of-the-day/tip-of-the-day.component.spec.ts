import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TipOfTheDayComponent } from './tip-of-the-day.component';

describe('TipOfTheDayComponent', () => {
  let component: TipOfTheDayComponent;
  let fixture: ComponentFixture<TipOfTheDayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TipOfTheDayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TipOfTheDayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
