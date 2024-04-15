import React from "react"
import style from "./Charts.module.css"

const Charts = ({ src }) => {
  return (
    <div className={style.mainContainer}>
      <iframe src={src} className={style.iframe}/>
    </div>
  )
}

export default Charts
