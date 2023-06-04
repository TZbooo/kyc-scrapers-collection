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

    async addScraper(name, minCharacters, offset, limit, origin, collectRetro) {
        const response = await $api.post(`/scrapers/${this.type.description}`, {
            id: crypto.randomUUID(),
            name: name,
            minCharacters: minCharacters,
            offset: offset,
            limit: limit,
            origin: origin,
            collectRetro: collectRetro,
            total: 0,
            totalPerMonth: 0,
            totalPerDay: 0,
            isRunning: true,
        });
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

    async deleteScraper(id) {
        await $api.delete(`/scrapers/${this.type.description}/${id}`);
    }

    async setRunningStatus(id, status) {
        const response = await $api.patch(
            `/scrapers/${this.type.description}/${id}`,
            {
                isRunning: status,
            }
        );
        const currentRunningStatus = response.data.isRunning;
        return currentRunningStatus;
    }
}

export default ScrapersService;
