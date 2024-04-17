import React from "react"
import { useState } from "react"
import { useEffect } from "react"
import style from "./ResInfo.module.css"
import { useStoreon } from "storeon/react"
import useApi from "../../Hooks/useApi"
import CommentsComponent from "../../components/CommentsComponent/CommentsComponent"
import MenuItem from "../../components/MenuItem/MenuItem"

const ResInfo = (restaurant_id) => {

  restaurant_id = "cayala@trefratelli.com"

  const api = useApi()
  const { user } = useStoreon("user")
  const [resInfo, setResInfo] = useState(null)
  const [menu, setMenu] = useState(null)
  const [horario, setHorario] = useState("horario")
  const [precios, setPrecios] = useState("precios")

  // datos del restaurante que se mostrarán en la página
  const gettingUserInfo = async () => {
    let response_user_info
    response_user_info = await api.handleRequest(
      "GET",
      "get/restaurant?restaurant_id=" + restaurant_id // esto en realidad no está bien. 
    )
    const data = await response_user_info // Recibidos
    setResInfo(data[0])
  }

  const gettingMenu = async () => {
    let response_menu
    response_menu = await api.handleRequest(
      "GET",
      "restaurant/dishes?restaurant_id=" + restaurant_id
    )
    const data = await response_menu // Recibidos
    setMenu(data)
  }

  useEffect(() => {
    gettingUserInfo()
    gettingMenu()


    // split schedule. get two parts. before - and after (including -). Add "hrs" to both of them at the end of each. 
    if (resInfo) {
      let horario = resInfo.schedule.split("-")
      setHorario(horario[0] + "hrs - " + horario[1] + "hrs")

      let precios = resInfo.prices.split("-")
      setPrecios("Q." + precios[0] + ".00 - Q." + precios[1] + ".00")
    }

  }, [])

  console.log("menu: \n", menu)
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

        <CommentsComponent comments={["hola mundo", "hola mundo", "hola mundo"]} />

      </div>
      <div className={style.rightContainer}>
        <h2>Menú</h2>
        <div className={style.menuContainer}>
          {menu ? (
            menu.map((item) => {
              return (
                <MenuItem
                  key={item.dish_id}
                  name={item.name}
                  price={item.price}
                  description={item.description}
                />
              )
            })
          ) : (
            <p>Cargando Menú</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default ResInfo