import React from "react"
import style from "./AddVisit.module.css"
import useApi from "../../Hooks/useApi"
import { useState } from "react"
import { useEffect } from "react"
import { useStoreon } from "storeon/react"
import ComponentInput from "../../components/Input/Input"
import TextAreaAuto from "../../components/textAreaAutosize/TextAreaAuto"

const AddVisit = (restaurant_id) => {
  restaurant_id = "Pizza Hut"

  const api = useApi()
  const { user } = useStoreon("user")
  const [resInfo, setResInfo] = useState(null)

  const [total, setTotal] = useState("")
  const [rating, setRating] = useState("")
  const [comment, setComment] = useState("")

  const getResInfo = async () => {
    let res
    res = await api.handleRequest(
      "GET",
      "get/restaurant?restaurant_id=" + restaurant_id
    )
    const data = await res
    setResInfo(data[0])
  }

  useEffect(() => {
    getResInfo()
  }, [])

  console.log(resInfo)

  const handleInputVal = (e) => {
    const { name } = e.target
    switch (name) {
      case "total":
        setTotal(e.target.value)
        break
      case "rating":
        setRating(e.target.value)
        break
      case "comment":
        setComment(e.target.value)
        break
      default:
        break
    }
  }


    /**
     * Esto es lo que debe llevar el body de la petición POST para agregar una visita:
      {
        "user_id": "string",
        "restaurant_id": "string",
        "dishes": [
          "string"
        ],
        "date": "2024-04-17T07:04:46.822Z",
        "total": 0,
        "rating": 0,
        "comment": "string"
      }
     */

    return (
      <div className={style.mainContainer}>
        <div className={style.upContainer}>
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
          <div className={style.resInfoContainer}>
            <h1>{resInfo && resInfo.name}</h1>
          </div>
        </div>

        <div className={style.downContainer}>
          <div className={style.numberInputs}>
          <div className={style.totalInputCont}>
            <span>Ingresa el total de la factura</span>
            <ComponentInput
              type="number"
              placeholder="Total"
              name="total"
              value={total}
              onChange={handleInputVal}
            />
          </div>
          <div className={style.ratingInputCont}>
            <span>Ingresa tu calificación</span>
            <ComponentInput
              type="number"
              placeholder="Rating"
              name="rating"
              value={rating}
              onChange={handleInputVal}
            />
          </div>
          </div>
          <div className={style.commentInputCont}>
            <span>Ingresa un comentario</span>
            <TextAreaAuto
              placeholder="Comentario"
              name="comment"
              value={comment}
              maxRows={8}
              onChange={handleInputVal}
            />
          </div>
        </div>
      </div>
    )
  }

  export default AddVisit