import { makeAutoObservable } from "mobx";

class ScrapersDataStore {
    tgScrapersData = [];
    webSiteScrapersData = [];

    constructor() {
        makeAutoObservable(this);
    }

    setTgScrapersData(data) {
        this.tgScrapersData = data;
    }

    setWebSiteScrapersData(data) {
        this.webSiteScrapersData = data;
    }
}

export default ScrapersDataStore;
