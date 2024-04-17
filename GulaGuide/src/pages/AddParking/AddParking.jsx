import React, { useEffect, useState } from "react"
import styles from "./AddParking.module.css"
import useApi from "../../Hooks/useApi"
import Header from "../../components/Header/Header"
import ValueList from "../../components/ValueList/ValueList"
import { useStoreon } from "storeon/react"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import Popup from "../../components/Popup/Popup"
import Checkbox from "@mui/material/Checkbox"

const AddParking = () => {
  const apiParking = useApi()
  const api = useApi()
  const { user } = useStoreon("user")

  const [parking, setParking] = useState()
  const [parkings, setParkings] = useState([])
  const [valletParking, setValletParking] = useState(false)
  const [freeHours, setFreeHours] = useState()
  const [exclusive, setExclusive] = useState(false)
  const [warning, setWarning] = useState(false)
  const [typeError, setTypeError] = useState(1)
  const [error, setError] = useState("")

  const getParkings = async () => {
    const response = await apiParking.handleRequest("GET", "get/parkingsAll")
    setParkings(response.data)
  }

  const handleParking = (e, newValue) => {
    setParking(newValue)
  }

  const addParking = async () => {
    const response = await api.handleRequest("POST", "restaurant/parking", {
      restaurant_id: user.id_user,
      parking_id: parking,
      vallet_parking: valletParking,
      free_hours: freeHours,
      exclusive: exclusive,
    })
    const data = response
    if (data.status === 200) {
      setTypeError(3)
      setWarning(true)
      setError("Parqueo agregado correctamente")
    } else {
      setTypeError(1)
      setWarning(true)
      setError("Ocurrió un error al agregar el parqueo")
    }
  }

  const handleClick = () => {
    addParking()
  }

  const handleValues = (e) => {
    switch (e.target.name) {
      case "valletParking":
        setValletParking(e.target.checked)
        break
      case "freeHours":
        setFreeHours(e.target.value)
        break
      case "exclusive":
        setExclusive(e.target.checked)
        break
      default:
        break
    }
  }

  useEffect(() => {
    getParkings()
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
          <span>Nombre del parqueo</span>
          <ValueList
            value={parking}
            placeholder="Nombre del platillo"
            options={parkings}
            onChange={handleParking}
          />
        </div>
        <div className={styles.inputContainer}>
          <span>¿Tiene vallet parking?</span>
          <Checkbox name="valletParking" onChange={handleValues} />
        </div>
        <div className={styles.inputContainer}>
          <span>Horas de cortesía</span>
          <ComponentInput
            name="freeHours"
            type="number"
            min={0}
            value={freeHours}
            placeholder="Horaio de inicio"
            onChange={handleValues}
          />
        </div>
        <div className={styles.inputContainer}>
          <span>Es propio</span>
          <Checkbox name="exclusive" onChange={handleValues} />
        </div>
        <div className={styles.inputContainer}>
          <Button label="Agregar parqueo" onClick={handleClick} />
        </div>
      </div>
    </div>
  )
}

export default AddParking
