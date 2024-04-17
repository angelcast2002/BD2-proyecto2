import React from "react"
import style from "./AddVisit.module.css"
import useApi from "../../Hooks/useApi"
import { useState } from "react"
import { useEffect } from "react"
import { useStoreon } from "storeon/react"
import ComponentInput from "../../components/Input/Input"
import TextAreaAuto from "../../components/textAreaAutosize/TextAreaAuto"
import ValueList from "../../components/ValueList/ValueList"
import Button from "../../components/Button/Button"
import Header from "../../components/Header/Header"


const AddVisit = ({ restaurant_id }) => {

  const api = useApi()
  const { user } = useStoreon("user")
  const user_id = user.id_user

  const [resInfo, setResInfo] = useState(null)
  const [dishes, setDishes] = useState(null)

  const [total, setTotal] = useState("")
  const [rating, setRating] = useState("")
  const [comment, setComment] = useState("")
  const [selectedDishes, setSelectedDishes] = useState([])

  const getResInfo = async () => {
    let res
    console.log("entro")
    res = await api.handleRequest(
      "GET",
      "get/restaurant?restaurant_id=" + restaurant_id
    )
    const data = await res
    console.log("data res info", data)
    setResInfo(data[0])
  }

  const getResDishes = async () => {
    let res
    res = await api.handleRequest(
      "GET",
      "restaurant/dishes?restaurant_id=" + restaurant_id
    )
    const data = await res
    setDishes(data.data)
  }

  useEffect(() => {
    getResInfo()
    getResDishes()
  }, [])

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

  const handleAddVisit = async () => {
    console.log("Agregando visita")
    console.log("user_id", user_id)
    console.log("restaurant_id", restaurant_id)
    console.log("selectedDishes", selectedDishes)
    console.log("total", total)
    console.log("rating", rating)
    console.log("comment", comment)

    const response = await api.handleRequest(
      "POST",
      "diner/visit",
      {
        user_id: user_id,
        restaurant_id: restaurant_id,
        dishes: selectedDishes,
        date: new Date(),
        total: total,
        rating: rating,
        comment: comment
      }
    )
    const data = await response
    console.log("data de la visita ->", data)
  }

  const handleChangeDishes = (e, newValue) => {
    setSelectedDishes(newValue);
  }

  return (
    <div className={style.mainContainer}>
      <Header />
      <div className={style.mainContainer2}>
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
          <div className={style.selectDishesContainer}>
            <span>Elige el platillo o platillos que has consumido</span>
            {dishes && (
              <ValueList
                options={dishes.map((dish) => dish.name)}
                value={selectedDishes}
                onChange={handleChangeDishes}
                placeholder="Platillos"
                multiple
              />
            )}
          </div>
          <div className={style.submitBtnContainer}>
            <Button label="Agregar visita" onClick={handleAddVisit} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default AddVisit