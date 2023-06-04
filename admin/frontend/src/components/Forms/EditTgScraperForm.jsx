import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import Form from "./Form";
import TextInput from "./TextInput";
import Checkbox from "./Checkbox";

const EditTgScraperForm = ({ tgScraperId, disable, disableSetter }) => {
    const [channelLink, setChannelLink] = useState("");
    const [channelLinkError, setChannelLinkError] = useState("");

    const [offset, setOffset] = useState("");
    const [offsetError, setOffsetError] = useState("");

    const [limit, setLimit] = useState("");
    const [limitError, setLimitError] = useState("");

    const [minCharacters, setMinCharacters] = useState("");
    const [minCharactersError, setMinCharactersError] = useState("");
    const [collectRetro, setCollectRetro] = useState(true);

    useEffect(() => {
        setChannelLinkError(validateChannelLink(channelLink));
        setOffsetError(validatePositiveNumberInput(offset));
        setLimitError(validatePositiveNumberInput(limit));
        setMinCharactersError(validatePositiveNumberInput(minCharacters));
    }, [channelLink, offset, limit, minCharacters]);

    return (
        <>
            <Form
                header='Изменить парсер'
                buttonText='Сохранить и перезапустить'
                disable={disable}
                disableSetter={disableSetter}
            >
                <input type='hidden' value={tgScraperId} name='tg_scraper_id' />
                <TextInput
                    placeholder='Ссылка на канал'
                    value={channelLink}
                    valueSetter={setChannelLink}
                    error={channelLinkError}
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
};

EditTgScraperForm.propTypes = {
    tgScraperId: PropTypes.string.isRequired,
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

export default EditTgScraperForm;
