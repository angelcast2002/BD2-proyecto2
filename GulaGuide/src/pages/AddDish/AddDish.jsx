import React, { useEffect, useState } from "react"
import styles from "./AddDish.module.css"
import useApi from "../../Hooks/useApi"
import Header from "../../components/Header/Header"
import ValueList from "../../components/ValueList/ValueList"
import { useStoreon } from "storeon/react"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import Popup from "../../components/Popup/Popup"

const AddDish = () => {
  const apiDish = useApi()
  const api = useApi()
  const { user } = useStoreon("user")

  const [dish, setDish] = useState()
  const [dishes, setDishes] = useState([])
  const [price, setPrice] = useState()
  const [cost, setCost] = useState()
  const [inicio, setInicio] = useState()
  const [fin, setFin] = useState()
  const [warning, setWarning] = useState(false)
  const [typeError, setTypeError] = useState(1)
  const [error, setError] = useState("")

  const getDishes = async () => {
    const response = await apiDish.handleRequest("GET", "get/dishesAll")
    setDishes(response.data)
  }

  const handleDish = (e, newValue) => {
    setDish(newValue)
  }

  const addDish = async () => {
    console.log(cost)
    const response = await api.handleRequest("POST", "restaurant/sells", {
      restaurant_id: user.id_user,
      dish_id: dish,
      price: price,
      sell_time: inicio.toString() + "-" + fin.toString(),
      cost: cost,
    })
    const data = response
    if (data.status === 200) {
      setTypeError(3)
      setWarning(true)
      setError("Platillo agregado correctamente")
    } else {
      setTypeError(1)
      setWarning(true)
      setError("Ocurrió un error al agregar el platillo")
    }
  }

  const handleClick = () => {
    addDish()
  }

  const handleValues = (e) => {
    switch (e.target.name) {
      case "price":
        setPrice(e.target.value)
        break
      case "cost":
        setCost(e.target.value)
        break
      case "inicio":
        setInicio(e.target.value)
        break
      case "fin":
        setFin(e.target.value)
        break
      case "costo":
        setCost(e.target.value)
        break
      default:
        break
    }
  }

  useEffect(() => {
    getDishes()
  }, [])

  return (
    <div className={styles.mainContainer}>
      <Header />
      <Popup
        message={error}
        status={warning}
        style={typeError}
        close={() => setWarning(false)}
      />
      <div className={styles.dataContainer}>
        <div className={styles.inputContainer}>
          <span>Nombre del platillo</span>
          <ValueList
            value={dish}
            placeholder="Nombre del platillo"
            options={dishes}
            onChange={handleDish}
          />
        </div>
        <div className={styles.inputContainer}>
          <span>Precio</span>
          <ComponentInput
            name="price"
            type="number"
            value={price}
            placeholder="Precio del platillo"
            onChange={handleValues}
          />
        </div>
        <div className={styles.inputContainer}>
          <span>Horario de venta</span>
          <ComponentInput
            name="inicio"
            type="number"
            min={0}
            max={24}
            value={inicio}
            placeholder="Horaio de inicio"
            onChange={handleValues}
          />
          <ComponentInput
            name="fin"
            type="number"
            min={0}
            max={24}
            value={fin}
            placeholder="Horaio de fin"
            onChange={handleValues}
          />
        </div>
        <div className={styles.inputContainer}>
          <span>Precio de elaboración</span>
          <ComponentInput
            name="costo"
            type="number"
            value={cost}
            placeholder="Costo del platillo"
            onChange={handleValues}
          />
        </div>
        <div className={styles.inputContainer}>
          <Button label="Agregar platillo" onClick={handleClick} />
        </div>
      </div>
    </div>
  )
}

export default AddDish
