import axios from "axios";
import AsyncStorage from '@react-native-async-storage/async-storage';
const SERVER_CONTEXT = "/QLDiemSinhVien";

export const endpoints = {
    
    "tinhDiemTB":`${SERVER_CONTEXT}/api/TinhDiemTB_SV/`,  
}

export const AuthApis = () => {
    return axios.create({
        baseURL: "http://127.0.0.1:8000",
        headers: {
            "Authorization": AsyncStorage.getItem('Token')
        }
    })
}

export default axios.create({
    baseURL: "http://127.0.0.1:8000"
})