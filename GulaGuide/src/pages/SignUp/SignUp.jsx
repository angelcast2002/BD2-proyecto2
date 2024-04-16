import React, { useState } from "react"
import style from "./SignUp.module.css"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import { navigate } from "../../store"
import Loader from "../../components/Loader/Loader"
import useApi from "../../Hooks/useApi"
import Popup from "../../components/Popup/Popup"
import Switch from "../../components/Switch/Switch"
import Checkbox from "@mui/material/Checkbox"
import { useStoreon } from "storeon/react"

// pedir correo, password, nombre, apellido, pfp
const SignUp = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [pfpPreview, setPfpPreview] = useState("/images/pfp.svg")
  const { dispatch } = useStoreon("user")
  const api = useApi()

  const [passWord, setPassWord] = useState("")
  const [email, setEmail] = useState("")
  const [nombres, setNombres] = useState("")
  const [apellidos, setApellidos] = useState("")
  const [fechaNacimiento, setFechaNacimiento] = useState("")
  const [genre, setGenre] = useState(false)
  const [url, setUrl] = useState("")
  const [presupuesto, setPresupuesto] = useState(0)
  const [vehiculo, setVehiculo] = useState(false)
  const [minimo, setMinimo] = useState(0)
  const [maximo, setMaximo] = useState(0)
  const [alcohol, setAlcohol] = useState(false)
  const [pet, setPet] = useState(false)
  const [apertura, setApertura] = useState(0)
  const [cierre, setCierre] = useState(0)

  const [warning, setWarning] = useState(false)
  const [error, setError] = useState("")
  const [typeError, setTypeError] = useState(1)

  const handlePassword = () => {
    setShowPassword(!showPassword)
  }

  const handleHome = () => {
    navigate("/")
  }

  const handleInputsValue = (e) => {
    switch (e.target.name) {
      case "correo":
        setEmail(e.target.value)
        break
      case "password":
        setPassWord(e.target.value)
        break
      case "nombres":
        setNombres(e.target.value)
        break
      case "apellidos":
        setApellidos(e.target.value)
      case "fechaNacimiento":
        setFechaNacimiento(e.target.value)
        break
      case "url":
        setUrl(e.target.value)
        setPfpPreview(e.target.value)
        break
      case "presupuesto":
        setPresupuesto(e.target.value)
        break
      case "vehiculo":
        setVehiculo(e.target.checked)
        break
      case "minimo":
        setMinimo(e.target.value)
        break
      case "maximo":
        setMaximo(e.target.value)
        break
      case "alcohol":
        setAlcohol(e.target.checked)
        break
      case "pet":
        setPet(e.target.checked)
        break
      case "apertura":
        setApertura(e.target.value)
        break
      case "cierre":
        setCierre(e.target.value)
        break
      default:
        break
    }
  }

  const handleSignUp = async () => {
    if (nombres === "" || email === "" || passWord === "") {
      setError("Los campos nombres, correo y contraseña son obligatorios")
      setTypeError(2)
      setWarning(true)
    } else {
      let response
      if (genre) {
        response = await api.handleRequest("POST", "user/signup/restaurant", {
          user_id: email,
          password: passWord,
          name: nombres,
          prices: (minimo + "-" + maximo).toString(),
          rating: 0,
          schedule: (apertura + "-" + cierre).toString(),
          sells_alcohol: alcohol,
          petFriendly: pet,
          imagen: url,
        })
        dispatch("user/config", {
          role: "restaurant",
          id_user: email,
        })
      } else {
        response = await api.handleRequest("POST", "user/signup/diner", {
          user_id: email,
          password: passWord,
          name: nombres,
          lastname: apellidos,
          birthdate: fechaNacimiento,
          spending: presupuesto,
          has_car: vehiculo,
          image: url,
        })
        dispatch("user/config", {
          role: "diner",
          id_user: email,
        })
      }
      const data = response
      if (data.status === 200) {
        setIsLoading(true)
        setError("Cuenta creada exitosamente, redirigiendo...")
        setTypeError(3)
        setWarning(true)
        setTimeout(() => {
          setIsLoading(false)
          navigate("/setsettings")
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

  const handleGenre = (e) => {
    setGenre(e.target.checked)
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
          <div className={style.imgContainer}>
            <img src={pfpPreview} alt="profile picture" />
          </div>
          <div className={style.dataContainer}>
            <div className={style.dataGroup1Container}>
              <div className={style.genreContainer}>
                <Switch value={genre} onClick={handleGenre} />
              </div>
              <div className={style.nameContainer}>
                <span>Url de Imágen</span>
                <ComponentInput
                  name="url"
                  type="text"
                  placeholder="url.com"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.nameContainer}>
                <span>Nombre</span>
                <ComponentInput
                  name="nombres"
                  type="text"
                  placeholder="Esteban"
                  onChange={handleInputsValue}
                />
              </div>
              <div
                className={style.lastNameContainer}
                style={{ display: genre ? "" : "none" }}
              >
                <span>Rango de precios</span>
                <div className={style.priceRangeContainer}>
                  <ComponentInput
                    name="minimo"
                    type="number"
                    placeholder="Mínimo"
                    onChange={handleInputsValue}
                  />
                  <ComponentInput
                    name="maximo"
                    type="number"
                    placeholder="Máximo"
                    onChange={handleInputsValue}
                  />
                </div>
              </div>
              <div
                className={style.lastNameContainer}
                style={{ display: genre ? "" : "none" }}
              >
                <span>Horario</span>
                <div className={style.priceRangeContainer}>
                  <ComponentInput
                    name="apertura"
                    type="number"
                    placeholder="Apertura"
                    onChange={handleInputsValue}
                  />
                  <ComponentInput
                    name="cierre"
                    type="number"
                    placeholder="Cierre"
                    onChange={handleInputsValue}
                  />
                </div>
              </div>
              <div
                className={style.lastNameContainer}
                style={{ display: genre ? "none" : "" }}
              >
                <span>Apellido</span>
                <ComponentInput
                  name="apellidos"
                  type="text"
                  placeholder="Nano"
                  onChange={handleInputsValue}
                />
              </div>
              <div
                className={style.birthDateContainer}
                style={{ display: genre ? "none" : "" }}
              >
                <span>Fecha de nacimiento</span>
                <ComponentInput
                  name="fechaNacimiento"
                  type="date"
                  placeholder="2018-07-22"
                  min="1940-01-01"
                  max="2005-01-01"
                  onChange={handleInputsValue}
                />
              </div>
            </div>
            <div className={style.dataGroup2Container}>
              <div className={style.emailContainer}>
                <span>Correo</span>
                <ComponentInput
                  name="correo"
                  type="text"
                  placeholder="uni@uni.com"
                  onChange={handleInputsValue}
                />
              </div>
              <div className={style.passwordContainer}>
                <span>Contraseña</span>
                <ComponentInput
                  name="password"
                  type="password"
                  placeholder="micontraseña123"
                  onChange={handleInputsValue}
                  eye
                  onClickButton={handlePassword}
                  isOpen={showPassword}
                />
              </div>
              <div
                className={style.emailContainer}
                style={{ display: genre ? "none" : "" }}
              >
                <span>Presupuesto promedio</span>
                <ComponentInput
                  name="presupuesto"
                  type="number"
                  placeholder="500"
                  onChange={handleInputsValue}
                />
              </div>
              <div
                className={style.emailContainer}
                style={{ display: genre ? "none" : "" }}
              >
                <span>¿Posee vehículo?</span>
                <Checkbox name="vehiculo" onChange={handleInputsValue} />
              </div>
              <div
                className={style.emailContainer}
                style={{ display: genre ? "" : "none" }}
              >
                <span>¿Vende alcohol?</span>
                <Checkbox name="alcohol" onChange={handleInputsValue} />
              </div>
              <div
                className={style.emailContainer}
                style={{ display: genre ? "" : "none" }}
              >
                <span>¿Acepta mascotas?</span>
                <Checkbox name="pet" onChange={handleInputsValue} />
              </div>
            </div>
            <div className={style.buttonContainer}>
              <Button label="Regresar" onClick={handleHome} size={"75%"} />
              <Button
                label="Crear cuenta"
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
