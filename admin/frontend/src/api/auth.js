import instance from "./instance";

export default class AuthService {
    static async checkAuth() {
        const response = await instance.get("/user/1");

        if (response.data?.auth) {
            return true;
        }
        return false;
    }
}
