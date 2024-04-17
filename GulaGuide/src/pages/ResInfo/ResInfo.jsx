import React from "react"
import { useState } from "react"
import { useEffect } from "react"
import style from "./ResInfo.module.css"
import { useStoreon } from "storeon/react"
import useApi from "../../Hooks/useApi"
import CommentsComponent from "../../components/CommentsComponent/CommentsComponent"
import MenuItem from "../../components/MenuItem/MenuItem"
import Loader from "../../components/Loader/Loader"
import Header from "../../components/Header/Header"

const ResInfo = ({ id }) => {
  const restaurant_id = id

  const api = useApi()
  const { user } = useStoreon("user")
  const [resInfo, setResInfo] = useState(null)
  const [menu, setMenu] = useState(null)
  const [horario, setHorario] = useState("")
  const [precios, setPrecios] = useState("")
  const [location, setLocation] = useState("")
  const [comments, setComments] = useState(null)

  const formatData = (data) => {
    let horario = data.schedule.split("-")
    setHorario(horario[0] + "hrs - " + horario[1] + "hrs")

    let precios = data.prices.split("-")
    setPrecios("Q." + precios[0] + ".00 - Q." + precios[1] + ".00")
  }
  // datos del restaurante que se mostrarán en la página
  const gettingUserInfo = async () => {
    let response_user_info
    response_user_info = await api.handleRequest(
      "GET",
      "get/restaurant?restaurant_id=" + restaurant_id // esto en realidad no está bien.
    )
    const data = await response_user_info // Recibidos
    formatData(data[0])
    setResInfo(data[0])
  }

  const gettingMenu = async () => {
    let response_menu
    response_menu = await api.handleRequest(
      "GET",
      "restaurant/dishes?restaurant_id=" + restaurant_id
    )
    const ans = await response_menu // Recibidos
    setMenu(ans.data)
  }

  const getLocation = async () => {
    let response_location
    response_location = await api.handleRequest(
      "GET",
      "restaurant/location?restaurant_id=" + restaurant_id
    )
    const ans = await response_location // Recibidos
    setLocation(ans.data)
  }

  const getComments = async () => {
    let response_comments
    response_comments = await api.handleRequest(
      "GET",
      "restaurant/comments?restaurant_id=" + restaurant_id
    )
    const ans = await response_comments // Recibidos
    setComments(ans)
  }

  useEffect(() => {
    gettingUserInfo()
    gettingMenu()
    getLocation()
    getComments()
  }, [])

  const handleAddVisit = async () => {
    // aqui se maneja ir hacia la página de añadir visita
    console.log("Presionando añadir visita")
  }

  const handleAddFavorite = async () => {
    // aqui se maneja añadir a favoritos
    console.log("Presionando añadir a favoritos")
  }

  return (
    <div className={style.mainContainer}>
      <Header />
      <div className={style.resInfoContainer}>
        {" "}
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
              <p className={style.address}>
                <strong>Dirección:</strong>{" "}
                {location
                  ? location.street +
                    ", " +
                    location.number +
                    ", " +
                    location.community
                  : "Cargando Dirección"}
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
              {resInfo && resInfo.petFriendly && <p> Acepta mascotas </p>}
              {resInfo && resInfo.sells_alcohol && (
                <p> Se puede consumir alcohol </p>
              )}
            </div>
          </div>
          <CommentsComponent comments={comments} />
          <div></div>
          <div className={style.buttonContainer}>
            <button className={style.visit} onClick={handleAddVisit}>
              Añadir visita
            </button>
            <button className={style.comment} onClick={handleAddFavorite}>
              Añadir a favoritos
            </button>
          </div>
        </div>
        <div className={style.rightContainer}>
          <h2>Menú</h2>
          <div className={style.menuContainer}>
            {Array.isArray(menu) &&
              menu.map((item, index) => {
                return (
                  <MenuItem
                    key={index}
                    name={item.name}
                    description={item.description}
                    avg_price={"Q." + item.avg_price + ".00"}
                  />
                )
              })}
          </div>
        </div>{" "}
      </div>
    </div>
  )
}

export default ResInfo
