import $api from "./instance";

export const ScraperTypes = Object.freeze({
    Telegram: Symbol("telegram"),
    WebSite: Symbol("site"),
});

class ScrapersService {
    constructor(type) {
        this.type = type;
    }

    async getList() {
        const response = await $api.get(`/scrapers/${this.type.description}`);
        return response.data;
    }

    async updateScraper(
        id,
        name,
        minCharacters,
        offset,
        limit,
        origin,
        collectRetro
    ) {
        const response = await $api.patch(
            `/scrapers/${this.type.description}/${id}`,
            {
                name: name,
                minCharacters: minCharacters,
                offset: offset,
                limit: limit,
                origin: origin,
                collectRetro: collectRetro,
            }
        );
        return response.data;
    }
}

export default ScrapersService;
