import React, { useState, useEffect } from "react"
import { navigate } from "../../store"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import styles from "./LogIn.module.css"
import Popup from "../../components/Popup/Popup"
import API_URL from "../../api"
import { useStoreon } from "storeon/react"
import useApi from "../../Hooks/useApi"
import { set } from "date-fns"

const LogIn = () => {
  const { dispatch } = useStoreon("user")

  const api = useApi()

  const [emailInput, setEmailInput] = useState("")
  const [passInput, setPassInput] = useState("")
  const [warning, setWarning] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [typeError, setTypeError] = useState(1)
  const [error, setError] = useState("")

  // Teniendo el DPI y la contraseña,necesitamos que nos devuelva un objeto usuario
  const logIn = async () => {
    const body = {
      usuario: emailInput,
      contra: passInput,
    }

    let response
    response = await api.handleRequest(
      "GET",
      "user/login?user_id=" + emailInput + "&password=" + passInput
    )

    const datos = await response // Recibidos

    if (datos.status === 200) {
      dispatch("user/config",
        {
          role: datos.role,
          id_user: emailInput
        }
      )
      
      setError("Sesión iniciada correctamente")
      setTypeError(3)
      setWarning(true)
      setTimeout(() => {
        if (datos.role === "Diner") navigate("/recommendations")
        else if (datos.role === "Admin")
        navigate("/homeadmin")
        else
        navigate("/edituser")
      }, 5000)
    } else if (datos.status === 400) {
      setError(datos.message)
      setTypeError(1)
      setWarning(true)
    } else {
      setError("Error de servidor")
      setTypeError(1)
      setWarning(true)
    }


  }

  const handleCorreo = (event) => {
    setEmailInput(event.target.value)
  }

  const handlePass = (event) => {
    setPassInput(event.target.value)
  }

  const handlePassword = () => {
    setShowPassword(!showPassword)
  }

  return (
    <div className={styles.logInCointainer}>
      <Popup
        message={error}
        status={warning}
        style={typeError}
        close={() => setWarning(false)}
      />
      <h1>GulaGuide</h1>
      <div className={styles.inputsContainer}>
        <div className={styles.usuarioContainer}>
          <span>Correo</span>
          <ComponentInput
            name="correo"
            type="text"
            placeholder="gulaguide@gmail.com"
            onChange={handleCorreo}
          />
        </div>
        <div className={styles.usuarioContainer}>
          <span>contraseña</span>
          <ComponentInput
            name="password"
            type="password"
            placeholder="micontraseña123"
            onChange={handlePass}
            eye
            onClickButton={handlePassword}
            isOpen={showPassword}
          />
        </div>
        <Button
          label="Iniciar Sesión"
          onClick={(event) => {
            event.preventDefault()
            logIn()
          }}
        />
        <a href="/signup">
          Eres nuevo?<span> Regístrate</span>
        </a>
      </div>
    </div>
  )
}

export default LogIn
