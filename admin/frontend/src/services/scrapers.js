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
        const response = await $api.get("/");
        return response.data;
    }

    async addScraper(name, minCharacters, offset, limit, origin, collectRetro) {
        const response = await $api.post("/", {
            name: name,
            is_running: true,
            min_characters: minCharacters,
            offset: offset,
            limit: limit,
            channel_link: origin,
            reverse: collectRetro,
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
        const response = await $api.put("/", {
            object_id: id,
            name: name,
            offset: offset,
            limit: limit,
            channel_link: origin,
            min_characters: minCharacters,
            reverse: collectRetro,
        });
        return response.data;
    }

    async deleteScraper(id) {
        await $api.delete("/", { data: { object_id: id } });
    }

    async setRunningStatus(id, status) {
        const response = await $api.patch("/is_running", {
            object_id: id,
            is_running: status,
        });
        const currentRunningStatus = response.data.is_running;
        return currentRunningStatus;
    }
}

export default ScrapersService;
