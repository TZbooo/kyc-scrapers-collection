import PropTypes from "prop-types";
import { useState, useEffect, useContext } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../App";
import ScrapersService, { ScraperTypes } from "../../services/scrapers";
import Form from "./Form";
import TextInput from "./TextInput";
import Checkbox from "./Checkbox";

const TelegramScraperAddForm = observer(({ disable, disableSetter }) => {
    const scrapersDataStore = useContext(ScrapersDataStoreContext);

    const [name, setName] = useState("");

    const [scraperOrigin, setScraperOrigin] = useState("");
    const [scraperOriginError, setScraperOriginError] = useState("");

    const [offset, setOffset] = useState("");
    const [offsetError, setOffsetError] = useState("");

    const [limit, setLimit] = useState("");
    const [limitError, setLimitError] = useState("");

    const [minCharacters, setMinCharacters] = useState("");
    const [minCharactersError, setMinCharactersError] = useState("");

    const [collectRetro, setCollectRetro] = useState(true);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const scrapersService = new ScrapersService(ScraperTypes.Telegram);
        const response = await scrapersService.addScraper(
            name,
            minCharacters,
            offset,
            limit,
            scraperOrigin,
            collectRetro
        );
        disableSetter(true);
        scrapersDataStore.tgScrapersData.push(response);
        setName("");
        setScraperOrigin("");
        setOffset("");
        setLimit("");
        setMinCharacters("");
    };

    useEffect(() => {
        setScraperOriginError(validateChannelLink(scraperOrigin));
        setOffsetError(validatePositiveNumberInput(offset));
        setLimitError(validatePositiveNumberInput(limit));
        setMinCharactersError(validatePositiveNumberInput(minCharacters));
    }, [scraperOrigin, offset, limit, minCharacters]);

    return (
        <>
            <Form
                header='Добавить новый парсер'
                buttonText='Добавить'
                handleSubmit={handleSubmit}
                disable={disable}
                disableSetter={disableSetter}
            >
                <TextInput
                    placeholder='Имя парсера'
                    value={name}
                    valueSetter={setName}
                />
                <TextInput
                    placeholder='Ссылка на канал'
                    value={scraperOrigin}
                    valueSetter={setScraperOrigin}
                    error={scraperOriginError}
                />
                <TextInput
                    placeholder='Оффсет'
                    value={offset}
                    valueSetter={setOffset}
                    error={offsetError}
                />
                <TextInput
                    placeholder='Лимит'
                    value={limit}
                    valueSetter={setLimit}
                    error={limitError}
                    required={false}
                />
                <TextInput
                    placeholder='Минимальное количество символов'
                    value={minCharacters}
                    valueSetter={setMinCharacters}
                    error={minCharactersError}
                />
                <Checkbox
                    placeholder='Ретроспектива'
                    checked={collectRetro}
                    checkedSetter={setCollectRetro}
                />
            </Form>
        </>
    );
});

TelegramScraperAddForm.propTypes = {
    disable: PropTypes.bool.isRequired,
    disableSetter: PropTypes.func.isRequired,
};

const validateChannelLink = (channelLink) => {
    const channelLinkMustStartWith = "https://t.me/";

    if (
        channelLinkMustStartWith.slice(0, channelLink.length) !==
        channelLink.slice(0, channelLinkMustStartWith.length)
    ) {
        return "Ссылка на канал должна начинаться с https://t.me/";
    } else {
        return false;
    }
};

const validatePositiveNumberInput = (value) => {
    if (!value) {
        return false;
    }

    if (isNaN(parseInt(value))) {
        return "Поле должно быть числом";
    }

    if (parseInt(value) < 0) {
        return "Поле должно быть больше нуля";
    }
};

export default TelegramScraperAddForm;
