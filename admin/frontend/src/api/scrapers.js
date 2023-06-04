import $api from "./instance";

export const ScraperTypes = Object.freeze({
    Tg: Symbol("tg"),
    WebSite: Symbol("site"),
});

class ScrapersService {
    constructor(type) {
        this.type = type;
    }

    async getList() {
        const response = await $api.get(`/scrapers/${this.type.description}`);
        console.log(response.data);
        return response.data;
    }
}

export default ScrapersService;
