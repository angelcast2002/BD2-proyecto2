import React, { useState, useEffect } from "react"
import cssStyle from "./Popup.module.css"

const Popup = ({ message, status, style, close }) => {

  // Si showPopup es false, el componente no se renderizará
  if (!status) {
    return null
  }

  useEffect(() => {
    setTimeout(() => {
      close()
    }, 5000)
  }, [])

  let image = "/images/check.svg"
  let backgroundColor = "#00b300"

  switch (style) {
    case 1:
      // Error
      image = "/images/error.svg"
      backgroundColor = "#e25959"
      break
    case 2:
      // Warning
      image = "/images/warning.svg"
      backgroundColor = "#e2c459"
      break
    case 3:
      // Ok
      image = "/images/check.svg"
      backgroundColor = "#00b300"
      break
    default:
      break
  }

  return (
    <div
    className={cssStyle.mainContainer}
      style={{ backgroundColor: backgroundColor }}
    >
      <div className={cssStyle.imgContainer}>
        <img src={image} alt="image" className={cssStyle.image} />
      </div>
      <div className={cssStyle.messageContainer}>
        <span className={cssStyle.span}>{message}</span>
      </div>
    </div>
  )
}

export default Popup
