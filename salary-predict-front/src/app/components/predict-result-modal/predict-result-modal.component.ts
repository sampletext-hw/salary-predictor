import {Component, Inject, OnInit} from '@angular/core';
import {PredictResponse} from "../../interfaces/predict-response";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-predict-result-modal',
  templateUrl: './predict-result-modal.component.html',
  styleUrls: ['./predict-result-modal.component.scss']
})
export class PredictResultModalComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<PredictResultModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: PredictResponse,
  ) {
  }

  ngOnInit(): void {
  }

  onClose() {
    this.dialogRef.close()
  }
}
