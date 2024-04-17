import React, { useEffect, useState } from "react"
import style from "./EditUser.module.css"
import { useStoreon } from "storeon/react"
import ComponentInput from "../../components/Input/Input"
import { Checkbox } from "@mui/material"
import useApi from "../../Hooks/useApi"
import { navigate } from "../../store"
import { set } from "date-fns"
import Button from "../../components/Button/Button"
import Header from "../../components/Header/Header"
import Popup from "../../components/Popup/Popup"


const EditUser = () => {

  const api = useApi()

  const { user } = useStoreon("user")
  const [datos_user_info, setDatos_user_info] = useState(null)


  const [url, setUrl] = useState("url")

  const [name, setName] = useState("nombre")
  const [lastname, setLastname] = useState("apellido")
  const [budget, setBudget] = useState(100)
  const [hasCar, setHasCar] = useState(false)
  const [pfp, setPfp] = useState("url")

  const [minPrice, setMinPrice] = useState("5")
  const [maxPrice, setMaxPrice] = useState("10")
  const [minSchedule, setMinSchedule] = useState("10")
  const [maxSchedule, setMaxSchedule] = useState("20")
  const [petFriendly, setPetFriendly] = useState(false)
  const [sellsAlcohol, setSellsAlcohol] = useState(false)

  const [error, setError] = useState("")
  const [warning, setWarning] = useState(false)
  const [typeError, setTypeError] = useState("")

  function splitByDash(text) {
    const parts = text.split('-');
    return [parts[0], parts.slice(1).join('-')];
  }

  const gettingUserInfo = async () => {
    let response_user_info
    response_user_info = await api.handleRequest(
      "GET",
      "user/get?user_id=" + user.id_user
    )

    const data = await response_user_info // Recibidos
    setDatos_user_info(data)
  }


  useEffect(() => {
    gettingUserInfo()
  }, [])

  console.log("datos_user_info ->", datos_user_info)

  useEffect(() => {
    if (datos_user_info) {
      if (user.role === "Diner") {
        console.log("AQUI!", datos_user_info)
        setUrl(datos_user_info.image);
        setPfp(datos_user_info.image);
        setName(datos_user_info.name);
        setLastname(datos_user_info.lastname);
        setBudget(datos_user_info.spending);
        setHasCar(datos_user_info.has_car);
      } else if (user.role === "Restaurant") {
        setUrl(datos_user_info.imagen);
        setPfp(datos_user_info.imagen);
        setName(datos_user_info.name);
        if (datos_user_info.schedule) {
          const [a, b] = splitByDash(datos_user_info.schedule);
          setMinSchedule(a);
          setMaxSchedule(b);
        }
        if (datos_user_info.prices) {
          const [c, d] = splitByDash(datos_user_info.prices);
          setMinPrice(c);
          setMaxPrice(d);
        }
        setPetFriendly(datos_user_info.petFriendly);
        setSellsAlcohol(datos_user_info.sells_alcohol);
      }
    }
  }, [datos_user_info]);

  const handleInputsValues = (e) => {
    const { name, value, checked } = e.target;
    switch (name) {
      case "url":
        setUrl(value)
        setPfp(value)
        break
      case "name":
        setName(e.target.value)
        break
      case "email":
        setEmail(e.target.value)
        break
      case "lastname":
        setLastname(e.target.value)
        break
      case "budget":
        setBudget(e.target.value)
        break
      case "hasCar":
        setHasCar(e.target.checked)
        break
      case "minPrice":
        setMinPrice(e.target.value)
        break
      case "maxPrice":
        setMaxPrice(e.target.value)
        break
      case "minSchedule":
        setMinSchedule(e.target.value)
        break
      case "maxSchedule":
        setMaxSchedule(e.target.value)
        break
      case "petFriendly":
        setPetFriendly(e.target.checked)
        break
      case "sellsAlcohol":
        setSellsAlcohol(e.target.checked)
        break
    }
  }

  const handleSaveChanges = async () => {
    if (user.role === "Diner") {
      const response = await api.handleRequest(
        "PUT",
        "user/update?user_id=" + user.id_user,
        {
          image: url,
          name: name,
          lastname: lastname,
          spending: budget,
          has_car: hasCar,
        }
      )

      const datos = await response // Recibidos
      if (datos.status === 200) {
        setError("Cambios guardados correctamente")
        setTypeError(3)
        setWarning(true)
      } else {
        setError("Error al guardar los cambios")
        setTypeError(1)
        setWarning(true)
      }

    }
    else if (user.role === "Restaurant") {
      const response = await api.handleRequest(
        "PUT",
        "user/update?user_id=" + user.id_user,
        {
          imagen: url,
          name: name,
          schedule: minSchedule + "-" + maxSchedule,
          prices: minPrice + "-" + maxPrice,
          petFriendly: petFriendly,
          sells_alcohol: sellsAlcohol,
        }
      )

      const datos = await response // Recibidos
      if (datos.status === 200) {
        setError("Cambios guardados correctamente")
        setTypeError(3)
        setWarning(true)
      } else {
        setError("Error al guardar los cambios")
        setTypeError(1)
        setWarning(true)
      }
    }

    

  }

  const handleDeleteUser = async () => {
    const response = await api.handleRequest(
      "DELETE",
      "user/delete?user_id=" + user.id_user
    )
    const datos = response // Recibidos
    console.log("datos de eliminacion ->", datos)
    if(datos.status === 200){
      setError("Usuario eliminado correctamente")
      setTypeError(3)
      setWarning(true)
      setTimeout(() => {
        navigate("/login")
      }, 5000)

    } else if (datos.status === 404){
      setError("El usuario ya ha sido eliminado")
      setTypeError(2)
      setWarning(true)
    } else {
      setError("Error al eliminar el usuario")
      setTypeError(1)
      setWarning(true)
    }
  }


  return (
    <div className={style.editUserContainer}>
      <Header />
      <Popup
        message={error}
        status={warning}
        style={typeError}
        close={() => setWarning(false)}
      />
      <div className={style.mainContainer}>
        <div className={style.imgContainer}>
          <img src={pfp} alt="profile picture" />
        </div>
        <div className={style.dataContainer}>
          {user.role === "Diner" && (
            <div className={style.dataGroup1Container}>
              <div className={style.urlContainer}>
                <span>URL de la foto de perfil</span>
                <ComponentInput
                  name="url"
                  type={"text"}
                  value={url}
                  onChange={handleInputsValues}
                />
              </div>
              <div className={style.nameContainer}>
                <span>Nombre</span>
                <ComponentInput
                  name="name"
                  type={"text"}
                  value={name}
                  onChange={handleInputsValues}
                />
              </div>
              <div className={style.lastnameContainer}>
                <span>Apellido</span>
                <ComponentInput
                  name="lastname"
                  type={"text"}
                  value={lastname}
                  onChange={handleInputsValues}
                />
              </div>
              <div className={style.budgetContainer}>
                <span>Presupuesto</span>
                <ComponentInput
                  name="budget"
                  type={"text"}
                  value={budget}
                  onChange={handleInputsValues}
                />
              </div>
              <div className={style.hascarContainer}>
                <span>¿Tienes auto?</span>
                <Checkbox
                  name="hasCar"
                  checked={hasCar}
                  onChange={handleInputsValues}
                />
              </div>
            </div>
          )}
          {user.role === "Restaurant" && (
            <div className={style.dataGroup2Container}>
              <div className={style.urlContainer}>
                <span>URL de la foto de perfil</span>
                <ComponentInput
                  name="url"
                  type={"text"}
                  value={url}
                  onChange={handleInputsValues}
                />
              </div>
              <div className={style.nameContainer}>
                <span>Nombre del Restaurante</span>
                <ComponentInput
                  name="name"
                  type={"text"}
                  value={name}
                  onChange={handleInputsValues}
                />
              </div>
              <div className={style.priceRangeContainer}>
                <span>Rango de Precios</span>
                <div className={style.priceRangeContainerInt}>
                  <ComponentInput
                    name="minPrice"
                    type={"text"}
                    placeholder={"Mínimo"}
                    value={minPrice}
                    onChange={handleInputsValues}
                  />
                  <ComponentInput
                    name="maxPrice"
                    type={"text"}
                    placeholder={"Máximo"}
                    value={maxPrice}
                    onChange={handleInputsValues}
                  />
                </div>
              </div>
              <div className={style.priceRangeContainer}>
                <span>Horario</span>
                <div className={style.priceRangeContainerInt}>
                  <ComponentInput
                    name="minSchedule"
                    type={"text"}
                    placeholder={"Mínimo"}
                    value={minSchedule}
                    onChange={handleInputsValues}
                  />
                  <ComponentInput
                    name="maxSchedule"
                    type={"text"}
                    placeholder={"Máximo"}
                    value={maxSchedule}
                    onChange={handleInputsValues}
                  />
                </div>
              </div>
              <div className={style.checkboxContainer}>
                <div className={style.priceRangeContainerInt}>
                  <span>¿Acepta mascotas?</span>
                  <Checkbox
                    name="petFriendly"
                    checked={petFriendly}
                    onChange={handleInputsValues}
                  />
                </div>
                <div className={style.priceRangeContainerInt}>
                  <span>¿Vende Alcohol?</span>
                  <Checkbox
                    name="sellsAlcohol"
                    checked={sellsAlcohol}
                    onChange={handleInputsValues}
                  />
                </div>
              </div>
            </div>
          )}
          <div className={style.buttonContainer}>
            <Button label="Eliminar Usuario" onClick={handleDeleteUser} size={"75%"} />
            <Button
              label="Guardar Cambios"
              onClick={handleSaveChanges}
              size={"75%"}
            />
          </div>
        </div>

      </div>
    </div>
  )
}

export default EditUser
