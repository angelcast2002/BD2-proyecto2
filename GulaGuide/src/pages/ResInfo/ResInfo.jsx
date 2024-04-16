import React from "react"
import style from "./ResInfo.module.css"
import { useStoreon } from "storeon/react"
import useApi from "../../Hooks/useApi"

const ResInfo = () => {

  const api = useApi()
  const { user } = useStoreon("user")
  const [resInfo, setResInfo] = React.useState(null)
  const [horario, setHorario] = React.useState("horario")
  const [precios, setPrecios] = React.useState("precios")

  // datos del restaurante que se mostrarán en la página
  const gettingUserInfo = async () => {
    let response_user_info
    response_user_info = await api.handleRequest(
      "GET",
      "get/restaurant?restaurant_id=" + user.id_user
    )
    const data = await response_user_info // Recibidos
    setResInfo(data[0])
  }

  React.useEffect(() => {
    gettingUserInfo()

    // split schedule. get two parts. before - and after (including -). Add "hrs" to both of them at the end of each. 
    if (resInfo) {
      let horario = resInfo.schedule.split("-")
      setHorario(horario[0] + "hrs - " + horario[1] + "hrs")

      let precios = resInfo.prices.split("-")
      setPrecios("Q." + precios[0] + ".00 - Q." + precios[1] + ".00")
    }



  }, [])


  console.log("user", user)
  console.log("resInfo", resInfo)

  return (
    <div className={style.resInfoContainer}>
      <div className={style.leftContainer}>
        <div className={style.imgContainer}>
          <img
            src={
              resInfo
                ? resInfo.imagen
                : "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg"
            }
            alt="Imagen del restaurante"
          />
        </div>
        <h1>{resInfo ? resInfo.name : "Cargando Nombre"}</h1>
        <div className={style.infoContainer}>
          <div className={style.textContainer}>
            <p>
              <strong>Dirección:</strong>{" "}
              {resInfo ? resInfo.address : "Cargando Dirección"}
            </p>
            <p className={style.rating}>
              <strong>Rating:</strong>{" "}
              {resInfo ? resInfo.rating : "Cargando Rating"}
            </p>
            <p>
              <strong>Horario:</strong>{" "}
              {resInfo ? horario : "Cargando Horario"}
            </p>
            <p>
              <strong>Precios:</strong>{" "}
              {resInfo ? precios : "Cargando Precios"}
            </p>
            {resInfo && resInfo.petFriendly && <p> Acepta Mascotas </p>}
            {resInfo && resInfo.sells_alcohol && <p> Se puede consumir alcohol </p>}
          </div>
          
        </div>
      </div>
      <div className={style.rightContainer}></div>
    </div>
  )
}

export default ResInfo