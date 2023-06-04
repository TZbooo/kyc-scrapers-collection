import PropTypes from "prop-types";
import { useContext } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../App";
import TableItem from "./TableItem";
import { ScraperTypes } from "../../services/scrapers";

const TableContent = observer(({ scraperType }) => {
    const scrapersDataStore = useContext(ScrapersDataStoreContext);

    if (scraperType === ScraperTypes.Telegram) {
        return (
            <>
                {scrapersDataStore.tgScrapersData.map((tableItem) => (
                    <TableItem
                        key={tableItem.id}
                        id={tableItem.id}
                        name={tableItem.name}
                        total={tableItem.total}
                        totalPerMonth={tableItem.totalPerMonth}
                        totalPerDay={tableItem.totalPerDay}
                        origin={tableItem.origin}
                        isRunning={tableItem.isRunning}
                    />
                ))}
            </>
        );
    }
    if (scraperType === ScraperTypes.WebSite) {
        return (
            <>
                {scrapersDataStore.webSiteScrapersData.map((tableItem) => (
                    <TableItem
                        key={tableItem.id}
                        id={tableItem.id}
                        name={tableItem.name}
                        total={tableItem.total}
                        totalPerMonth={tableItem.totalPerMonth}
                        totalPerDay={tableItem.totalPerDay}
                        origin={tableItem.origin}
                        isRunning={tableItem.isRunning}
                    />
                ))}
            </>
        );
    }
});

TableContent.propTypes = {
    scraperType: PropTypes.symbol.isRequired,
};

export default TableContent;
