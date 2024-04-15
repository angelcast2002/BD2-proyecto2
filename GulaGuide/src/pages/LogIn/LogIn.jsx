import React, { useState, useEffect } from "react"
import { navigate } from "../../store"
import ComponentInput from "../../components/Input/Input"
import Button from "../../components/Button/Button"
import styles from "./LogIn.module.css"
import Popup from "../../components/Popup/Popup"
import API_URL from "../../api"
import { useStoreon } from "storeon/react"

const LogIn = () => {
  const { dispatch } = useStoreon("user")

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
    const response = await fetch(`${API_URL}/api/login`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    })

    const datos = await response.json() // Recibidos

    if (datos.status === 200) {
      // Estado global
      const { token, role } = datos.data
      dispatch("user/config", {
        token,
        role,
        id_user: emailInput,
      })
      if (role === "student") {
        navigate("/profile")
      } else if (role === "enterprise") {
        navigate("/postulacionempresa")
      } else if (role === "admin") {
        navigate("/profileadmin")
      }
    } else if (datos.status === 403) {
      setTypeError(1)
      setError("Cuenta deshabilitada. Contacte al administrador")
      setWarning(true)
    } else {
      setTypeError(1)
      setError("Credenciales incorrectas. Inténtelo de nuevo")
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
