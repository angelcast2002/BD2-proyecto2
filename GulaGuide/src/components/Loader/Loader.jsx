import React from "react"
import style from "./Loader.module.css"

const Loader = ({ size }) => {
  const customStyle = [
    {
      "--d": "200ms",
    },
    {
      "--d": "400ms",
    },
    {
      "--d": "600ms",
    },
    {
      "--d": "800ms",
    },
    {
      "--d": "1000ms",
    },
  ]

  return (
    <div className={style.threebody}>
      <div className={style.threebody__dot} />
      <div className={style.threebody__dot} />
      <div className={style.threebody__dot} />
    </div>
  )
}

export default Loader
