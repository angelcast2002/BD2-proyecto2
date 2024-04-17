import React from "react"
import styles from "./InfoTab.module.css"
import Button from "../Button/Button"

const InfoTab = ({
  title,
  image,
  rangePrices,
  recomendations,
  location,
  schedule,
}) => {
  return <div className={styles.container}>
    <div className={styles.imageContainer}>
      <img src={image} alt="restaurant" />
    </div>
    <div className={styles.infoContainer}>
      <h3>{title}</h3>
      <div className={styles.info}>
        <p>{rangePrices}</p>
        <p>{recomendations}</p>
        <p>{location}</p>
        <p>{schedule}</p>
      </div>
    </div>
  </div>
}

export default InfoTab
