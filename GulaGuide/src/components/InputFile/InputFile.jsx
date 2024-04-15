import React, { useState } from "react"
import style from "./InputFile.module.css"

const InputFile = ({ file, placeHolder, onFileSelect, type }) => {
  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0]
    onFileSelect(selectedFile)
  }

  let accept = ""
  if (type === "pdf") {
    accept = ".pdf"
  } else if (type === "image") {
    accept = ".jpg, .jpeg, .png"
  } else {
    accept = ".pdf, .jpg, .jpeg, .png"
  }

  return (
    <div className={style.mainContainer}>
      <div
        className={style.fileContainer}
      >
        <label className={style.customFileInput}>
          <span className={style.textFile}>
            {file ? file : placeHolder}
          </span>
          <input
            type="file"
            accept={accept}
            className={style.fileInput}
            onChange={handleFileSelect}
          />
        </label>
      </div>
    </div>
  )
}

export default InputFile
