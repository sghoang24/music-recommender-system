import axios from "axios";

const api = axios.create({
    baseURL: "https://music-recommender-livid.vercel.app/",
    // baseURL: "http://localhost:8000/",
})

export default api