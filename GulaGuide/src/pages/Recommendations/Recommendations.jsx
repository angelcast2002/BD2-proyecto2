import React from "react"
import styles from "./Recommendations.module.css"
import Header from "../../components/Header/Header"
import InfoTab from "../../components/InfoTab/InfoTab"

const Recommendations = () => {
  return (
    <div className={styles.container}>
      <Header />
      <InfoTab 
        title="Restaurante 1"
        image="https://www.eluniversal.com.mx/sites/default/files/2020/04/07/restaurantes.jpg"
        rangePrices="Rango de precios: $100 - $500"
        recomendations="Recomendaciones: 4.5/5"
        location="Ubicación: Zona 10"
        schedule="Horario: 8:00 - 20:00"
      />
    </div>
  )
}

export default Recommendations
