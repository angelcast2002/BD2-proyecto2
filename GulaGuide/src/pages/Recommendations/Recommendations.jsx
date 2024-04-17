import React, { useEffect, useState } from "react"
import styles from "./Recommendations.module.css"
import Header from "../../components/Header/Header"
import InfoTab from "../../components/InfoTab/InfoTab"
import { useStoreon } from "storeon/react"
import useApi from "../../Hooks/useApi"
import Loader from "../../components/Loader/Loader"
import ComponentInput from "../../components/Input/Input"
import ValueList from "../../components/ValueList/ValueList"
import Button from "../../components/Button/Button"
import { navigate } from "../../store"

const Recommendations = () => {
  const { user } = useStoreon("user")

  const apiRecommendations = useApi()
  const apiZonas = useApi()

  const [recommendations, setRecommendations] = useState([])
  const [recomendationsCopy, setRecomendationsCopy] = useState([])
  const [loading, setLoading] = useState(false)
  const [nameFilter, setNameFilter] = useState("")
  const [zonas, setZonas] = useState([])
  const [zona, setZona] = useState("")
  const [rating, setRating] = useState("")

  const getRecommendations = async () => {
    const response = await apiRecommendations.handleRequest(
      "GET",
      "diner/recommend?user_id=" + user.id_user + "&limit=20"
    )

    const datos = await response
    console.log("Datos", datos)
    if (datos.status === 200) {
      setRecomendationsCopy(datos.data)
      setRecommendations(datos.data)
    }
    setLoading(false)
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

  const handleFilters = (e) => {
    switch (e.target.name) {
      case "nombre":
        setNameFilter(e.target.value)
        break
      default:
        break
    }
  }

  const filterData = () => {
    let filteredData = recomendationsCopy
    if (nameFilter !== "" && nameFilter !== null) {
      filteredData = filteredData.filter((data) => {
        console.log("Data", data)
        return data.name.toLowerCase().includes(nameFilter.toLowerCase())
      })
    }
    if (zona !== "" && zona !== null && zona.length > 0) {
      if (Array.isArray(zona)) {
        filteredData = filteredData.filter((data) =>
          zona.includes(data.location)
        )
      } else {
        filteredData = filteredData.filter((data) => data.location === zona)
      }
    }
    console.log("Rating", rating)
    if (rating !== "" && rating !== null && rating.length > 0) {
      if (Array.isArray(rating)) {
        filteredData = filteredData.filter((data) =>
          rating.includes(data.rating)
        )
      } else {
        filteredData = filteredData.filter((data) => data.rating === rating)
      }
    }
    console.log("Filtered data", filteredData)
    return filteredData
  }

  const handleClickRestaurant = (id) => () => {
    navigate("/resinfo/" + id)
  }

  const handleZona = (e, newValue) => {
    setZona(newValue)
  }

  const handleSearchButton = () => {
    setLoading(true)
    setRecommendations(filterData())
    setLoading(false)
  }

  const handleCleanFilters = () => {
    setNameFilter("")
    setRecommendations(recomendationsCopy)
  }

  const handleRating = (e, newValue) => {
    setRating(newValue)
  }

  useEffect(() => {
    setLoading(true)
    handleAllZones()
    getRecommendations()
  }, [])

  return (
    <div className={styles.container}>
      <Header />
      <div className={styles.infoContainer}>
        <div className={styles.filtrosContainer}>
          <div className={styles.filterContainer}>
            <span>Nombre del restaurante</span>
            <ComponentInput
              name="nombre"
              type="text"
              value={nameFilter}
              placeholder="Pizza hut"
              onChange={handleFilters}
            />
          </div>
          <div className={styles.filterContainer}>
            <span>Zona</span>
            <ValueList
              value={[zona]}
              placeholder="Zona 1"
              options={zonas}
              onChange={handleZona}
              multiple
            />
          </div>
          <div className={styles.filterContainer}>
            <span>Rating</span>
            <ValueList
              value={[rating]}
              placeholder="Rating"
              options={[1, 2, 3, 4, 5]}
              onChange={handleRating}
              multiple
            />
          </div>
          <div className={styles.filtersButtonContainer}>
            <Button label="Buscar" onClick={handleSearchButton} size={"70%"} />
            <Button label="Limpiar" onClick={handleCleanFilters} size={"70%"} />
          </div>
        </div>
        {loading ? (
          <div className={styles.loaderContainer}>
            <Loader />
          </div>
        ) : (
          <div
            className={styles.recommendationsContainer}
            style={
              loading && recommendations.length > 0 ? { display: "none" } : {}
            }
          >
            {recommendations.length > 0 ? (
              recommendations.map((recommendation) => {
                return (
                  <InfoTab
                    title={recommendation.name}
                    image={recommendation.imagen}
                    rangePrices={`Rango de precios: Q${recommendation.prices}`}
                    recomendations={`Rating: ${
                      recommendation.rating === -1
                        ? "Sin rating"
                        : recommendation.rating
                    }`}
                    location={`Zona: ${recommendation.location}`}
                    schedule={`Horario: ${recommendation.schedule}`}
                    onClick={handleClickRestaurant(recommendation.user_id)}
                  />
                )
              })
            ) : (
              <div className={styles.noResultsContainer}>
                <h1>No se encontraron resultados</h1>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Recommendations
