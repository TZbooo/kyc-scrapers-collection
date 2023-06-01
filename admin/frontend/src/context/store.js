import { makeAutoObservable } from "mobx";
import AuthService from "../api/auth";

export default class Store {
    isAuth = false;
    isLoading = false;
    userData = {};

    constructor() {
        makeAutoObservable(this, {}, { deep: true });
    }

    setIsAuth(bool) {
        this.isAuth = bool;
    }

    setIsLoading(bool) {
        this.isLoading = bool;
    }

    setUserData(data) {
        this.userData = data;
    }

    async checkAuth() {
        this.setIsLoading(true);
        try {
            const isAuth = await AuthService.checkAuth();
            this.setIsAuth(isAuth);
        } finally {
            this.setIsLoading(false)
        }
    }
}