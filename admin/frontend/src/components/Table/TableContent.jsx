import { useContext } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../App";
import TableItem from "./TableItem";

const TableContent = observer(() => {
    const scrapersDataStore = useContext(ScrapersDataStoreContext);

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
});

export default TableContent;
