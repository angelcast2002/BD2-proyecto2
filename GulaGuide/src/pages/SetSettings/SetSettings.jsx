import React, { useEffect, useState } from "react"
import style from "./SetSettings.module.css"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import { navigate } from "../../store"
import Loader from "../../components/Loader/Loader"
import useApi from "../../Hooks/useApi"
import Popup from "../../components/Popup/Popup"
import Switch from "../../components/Switch/Switch"
import Checkbox from "@mui/material/Checkbox"
import { useStoreon } from "storeon/react"
import TextArea from "../../components/textAreaAutosize/TextAreaAuto"
import ValueList from "../../components/ValueList/ValueList"

// pedir correo, password, nombre, apellido, pfp
const SignUp = () => {
  const [isLoading, setIsLoading] = useState(false)
  const apiZonas = useApi()
  const api = useApi()
  const { user } = useStoreon("user")

  const [calle, setCalle] = useState("")
  const [avenida, setAvenida] = useState("")
  const [numero, setNumero] = useState("")
  const [colonia, setColonia] = useState("")
  const [referencias, setReferencias] = useState("")
  const [zona, setZona] = useState("")
  const [zonas, setZonas] = useState([])

  const [warning, setWarning] = useState(false)
  const [error, setError] = useState("")
  const [typeError, setTypeError] = useState(1)

  console.log("-->", user.id_user)

  const handleInputsValue = (e) => {
    switch (e.target.name) {
      case "calle":
        setCalle(e.target.value)
        break
      case "avenida":
        setAvenida(e.target.value)
        break
      case "numero":
        setNumero(e.target.value)
        break
      case "colonia":
        setColonia(e.target.value)
        break
      case "referencias":
        setReferencias(e.target.value)
        break
      default:
        break
    }
  }

  const handleAllZones = async () => {
    const response = await apiZonas.handleRequest("GET", "get/location/all")
    console.log("Zonas", response)
    const data = response
    if (data.status === 200) {
      setZonas(data.data)
    } else {
      setError(data.message)
      setTypeError(1)
      setWarning(true)
    }
  }

  useEffect(() => {
    handleAllZones()
  }, [])

  const handleSignUp = async () => {
    console.log("Zona", zona)
    if (zona === "" || zona === null) {
      setError("El campo de zona es obligatorio")
      setTypeError(2)
      setWarning(true)
    } else {
      let response
      if (user.role === "restaurant") {
        response = await api.handleRequest("POST", "restaurant/location", {
          restaurant_id: user.id_user,
          street: calle,
          avenue: avenida,
          number: numero,
          community: colonia,
          reference: referencias,
          zone: zona,
        })
      } else {
        response = await api.handleRequest("POST", "diner/location", {
          diner_id: user.id_user,
          street: calle,
          avenue: avenida,
          number: numero,
          community: colonia,
          reference: referencias,
          zone: zona,
        })
      }
      const data = response
      if (data.status === 200) {
        setIsLoading(true)
        setError("Datos guardados exitosamente, redirigiendo...")
        setTypeError(3)
        setWarning(true)
        setTimeout(() => {
          setIsLoading(false)
          navigate("/recommendations")
        }, 5000)
      } else if (data.status === 404) {
        setError(data.message)
        setTypeError(2)
        setWarning(true)
      } else {
        setError(response.message)
        setTypeError(1)
        setWarning(true)
      }
      setIsLoading(false)
    }
  }

  const handleZona = (e, newValue) => {
    setZona(newValue)
  }

  return (
    <div className={style.signUpCointainer}>
      <Popup
        message={error}
        status={warning}
        style={typeError}
        close={() => setWarning(false)}
      />
      {isLoading ? (
        <div className={style.loaderContainer}>
          <Loader size={100} />
        </div>
      ) : (
        <div className={style.mainContainer}>
          <div className={style.dataContainer}>
            <div className={style.dataGroup2Container}>
              <div className={style.emailContainer}>
                <span>Calle</span>
                <ComponentInput
                  name="calle"
                  type="text"
                  placeholder="6 calle"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.passwordContainer}>
                <span>Avenida</span>
                <ComponentInput
                  name="avenida"
                  type="text"
                  placeholder="6 avenida"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.passwordContainer}>
                <span>Número</span>
                <ComponentInput
                  name="numero"
                  type="text"
                  placeholder="8-72"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.passwordContainer}>
                <span>Colonia</span>
                <ComponentInput
                  name="colonia"
                  type="text"
                  placeholder="San Isidro"
                  onChange={handleInputsValue}
                />
              </div>
            </div>
            <div className={style.dataGroup1Container}>
              <div className={style.passwordContainer}>
                <span>Referencias</span>
                <TextArea
                  name="referencias"
                  type="text"
                  placeholder="Casa blanca"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.passwordContainer}>
                <span>Zona</span>
                <ValueList
                  value={zona}
                  placeholder="Zona 1"
                  options={zonas}
                  onChange={handleZona}
                />
              </div>
            </div>
            <div className={style.buttonContainer}>
              <Button
                label="Continuar"
                onClick={handleSignUp}
                size={"75%"}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SignUp
