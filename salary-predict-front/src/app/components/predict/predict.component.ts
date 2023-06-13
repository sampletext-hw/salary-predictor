import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {PredictionService} from "../../services/prediction.service";
import {MatSnackBar} from "@angular/material/snack-bar";
import {PredictRequest} from "../../interfaces/predict-request";
import {MatDialog} from "@angular/material/dialog";
import {PredictResultModalComponent} from "../predict-result-modal/predict-result-modal.component";

enum Gender {
  "Female" = "0",
  "Male" = "1",
  "Other" = "2"
}

enum EduLevel {
  "bachelor's" = "0",
  "high school" = "1",
  "master's" = "2",
  "phd" = "3"
}

enum JobTitle {
  "A" = "0",
  "B" = "1",
  "C" = "2",
  "D" = "3",
  "E" = "4",
  "F" = "5",
  "G" = "6",
  "H" = "7",
  "I" = "8",
  "J" = "9",
  "M" = "10",
  "N" = "11",
  "O" = "12",
  "P" = "13",
  "R" = "14",
  "S" = "15",
  "T" = "16",
  "U" = "17",
  "V" = "18",
  "W" = "19"
}

type ISelect = {
  numericValue: string;
  stringValue: string;
}

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.scss']
})
export class PredictComponent implements OnInit {
  formGroup: FormGroup = new FormGroup({});

  // @ts-ignore
  genderSelect: ISelect[] = Object.keys(Gender).map(x => ({stringValue: x, numericValue: parseInt(Gender[x])}))
  // @ts-ignore
  eduLevelSelect: ISelect[] = Object.keys(EduLevel).map(x => ({stringValue: x, numericValue: parseInt(EduLevel[x])}))
  // @ts-ignore
  jobTitleSelect: ISelect[] = Object.keys(JobTitle).map(x => ({stringValue: x, numericValue: parseInt(JobTitle[x])}))
  isFormSent: boolean = false;

  constructor(
    private predictionService: PredictionService,
    private matSnackBar: MatSnackBar,
    public dialog: MatDialog,
  ) {
    this.formGroup = new FormGroup({
      'age': new FormControl(null, [Validators.required]),
      'gender': new FormControl(null, [Validators.required]),
      'edu_level': new FormControl(null, [Validators.required]),
      'job_title': new FormControl(null, [Validators.required]),
      'years_exp': new FormControl(null, [Validators.required])
    })
  }

  ngOnInit(): void {
  }

  submit() {
    if (!this.formGroup.valid) {
      this.formGroup.markAllAsTouched()
      this.matSnackBar.open('Заполните все поля', '', {duration: 3000})
      return;
    }
    this.isFormSent = true;
    const request: PredictRequest = {
      age: this.formGroup.value.age,
      gender: this.formGroup.value.gender,
      edu_level: this.formGroup.value.edu_level,
      job_title: this.formGroup.value.job_title,
      years_exp: this.formGroup.value.years_exp,
    }
    this.predictionService.predict(request)
      .subscribe({
        next: (r) => {
          const dialogRef = this.dialog.open(PredictResultModalComponent, {
            data: r,
            disableClose: false
          });
        },
        error: () => {
          this.isFormSent = false;
        },
        complete: () => {
          this.isFormSent = false;
        }
      })
  }
}
