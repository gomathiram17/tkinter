from tkinter import *
from tkinter import messagebox,Menu #for notification; it also has lot of functions(google it) and Menu is used for providing menu bar for the portfolio
import requests
import json
import sqlite3
cryptopy=Tk() #instance creation
cryptopy.title("my crypto Portfolio")
cryptopy.iconbitmap("C:\\Users\\91790\\Downloads\\smartphone_phone_chat_icon_142147.ico")

con= sqlite3.connect("coin.db")
cursorObj=con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()
#cursorObj.execute("insert into coin values(1,'BTC',2, 3250)")
#con.commit()
#cursorObj.execute("insert into coin values(2, 'ETH' ,5, 120)")
#con.commit()
#cursorObj.execute("insert into coin values(3, 'NEO' ,5, 10)")
#con.commit()
#cursorObj.execute("insert into coin values(4, 'XMR' ,3, 30)")
#con.commit()

#label is used to give size,color,position and other attributes; bg-background color ;fg-font color
#this program finds the profit and loss in the price
#instead of grid pack() can also be used but index cannot be given
def reset(): #while updating or deleting, to avoid overlapping of icons, we use this fn to destroy the entire data and rebuild the updated data
    for cell in cryptopy.winfo_children():  #winfo_children shows every window in the app. from headings to cells and every nook and corners
        cell.destroy()
    app_nav()
    app_header()
    myportfolio()

def app_nav():
    def clearport():
        cursorObj.execute("DELETE from coin")
        con.commit()
        messagebox.showinfo("Portfolio notification","Portfolio cleared-Add new coins")
        reset()
    def closeapp():
        cryptopy.destroy()

    menu= Menu(cryptopy)
    file_item= Menu(menu)
    file_item.add_command(label='clearportfolio',command= clearport)
    file_item.add_command(label='closeApp',command= closeapp)
    menu.add_cascade(label="File", menu=file_item)
    cryptopy.config(menu=menu)


def myportfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=cf46855b-314c-4233-8a0c-0f595298057b")
    api = json.loads(api_request.content)
    cursorObj.execute("SELECT * from coin")
    coins= cursorObj.fetchall()

    def fontcolor(amount): #for indicating profit and loss using green and red resp.
        if(amount>0):
            return "green"
        else:
            return "red"

    def insert_coin():
        cursorObj.execute("insert into coin(symbol,price,amount) VALUES(? , ?, ?)", (symbol_text.get(), price_text.get(), amt_text.get()))
        con.commit()
        messagebox.showinfo("Portfolio notification","Coin has been added successfully!!") #showinfo has 2 parameters ("heading","msg content")
        reset()

    def update_coin():
        cursorObj.execute("update coin set symbol=? , price=? ,amount=? WHERE id=?",(symbol_update.get() , price_update.get() , amt_update.get() , portid_update.get()))
        con.commit()
        messagebox.showinfo("Portfolio notification","Changes has been updated successfully!!")
        reset()

    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),)) #comma should be added at the end for single valued tuple
        con.commit()
        messagebox.showinfo("Portfolio notification","Coin has been deleted successfully!!")
        reset()

    total_pl = 0
    coin_row=1
    totcurrentval=0
    totamtpaid=0

    for i in range(0,300):
         for coin in coins:
              if api["data"][i]["symbol"] == coin[1]:
                   total_paid = coin[2] * coin[3]
                   current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                   pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                   total_pl_coin = pl_percoin * coin[2]

                   total_pl+= total_pl_coin
                   totcurrentval+=current_value
                   totamtpaid += total_paid

                   Portfolio_id=Label(cryptopy,text=coin[0],bg="#F3F4F6",fg="black",font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   Portfolio_id.grid(row=coin_row,column=0,sticky=N+S+E+W)

                   name=Label(cryptopy,text=api["data"][i]["symbol"],bg="#F3F4F6",fg="black",font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   name.grid(row=coin_row,column=1,sticky=N+S+E+W)

                   price=Label(cryptopy,text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]),bg="white",fg="black",font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   price.grid(row=coin_row,column=2,sticky=N+S+E+W)

                   coinowned=Label(cryptopy,text=coin[2],bg="#F3F4F6",fg="black",font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   coinowned.grid(row=coin_row,column=3,sticky=N+S+E+W)

                   amtpaid=Label(cryptopy,text="${0:.2f}".format(total_paid),bg="#F3F4F6",fg="black",font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   amtpaid.grid(row=coin_row,column=4,sticky=N+S+E+W)

                   currentval=Label(cryptopy,text="${0:.2f}".format(current_value),bg="#F3F4F6",fg="black",font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   currentval.grid(row=coin_row,column=5,sticky=N+S+E+W)

                   pl_coin=Label(cryptopy,text="${0:.2f}".format(pl_percoin),bg="#F3F4F6",fg=fontcolor(float("{0:.2f}".format(pl_percoin))),font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   pl_coin.grid(row=coin_row,column=6,sticky=N+S+E+W)

                   tot_pl=Label(cryptopy,text="${0:.2f}".format(total_pl_coin),bg="#F3F4F6",fg=fontcolor(float("{0:.2f}".format(total_pl_coin))),font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
                   tot_pl.grid(row=coin_row,column=7,sticky=N+S+E+W)
                   coin_row += 1

    #insertrow
    symbol_text=Entry(cryptopy, borderwidth=2 , relief="groove")
    symbol_text.grid(row= coin_row+1 ,column=1)

    price_text=Entry(cryptopy, borderwidth=2 , relief="groove")
    price_text.grid(row= coin_row+1 ,column=2)

    amt_text=Entry(cryptopy, borderwidth=2 , relief="groove")
    amt_text.grid(row= coin_row+1 ,column=3)

    addcoin=Button(cryptopy,text="add coin",bg="#142E54",fg="white",command=insert_coin,font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
    addcoin.grid(row=coin_row+1,column=4,sticky=N+S+E+W)

    #updatevalues

    portid_update=Entry(cryptopy, borderwidth=2 , relief="groove")
    portid_update.grid(row= coin_row+2 ,column=0)

    symbol_update=Entry(cryptopy, borderwidth=2 , relief="groove")
    symbol_update.grid(row= coin_row+2 ,column=1)

    price_update=Entry(cryptopy, borderwidth=2 , relief="groove")
    price_update.grid(row= coin_row+2 ,column=2)

    amt_update=Entry(cryptopy, borderwidth=2 , relief="groove")
    amt_update.grid(row= coin_row+2 ,column=3)

    update_coin_txt=Button(cryptopy,text="update coin",bg="#142E54",fg="white",command=update_coin,font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
    update_coin_txt.grid(row=coin_row+2,column=4,sticky=N+S+E+W)

    portid_delete=Entry(cryptopy, borderwidth=2 , relief="groove")
    portid_delete.grid(row= coin_row+3 ,column=0)

    delete_coin_txt=Button(cryptopy,text="delete coin",bg="#142E54",fg="white",command=delete_coin,font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
    delete_coin_txt.grid(row=coin_row+3 ,column=4 ,sticky=N+S+E+W)

    tot_ap=Label(cryptopy,text="${0:.2f}".format(totamtpaid),bg="#F3F4F6",fg=fontcolor(float("{0:.2f}".format(total_pl))),font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
    tot_ap.grid(row=coin_row,column=4,sticky=N+S+E+W)

    tot_pl=Label(cryptopy,text="${0:.2f}".format(total_pl),bg="#F3F4F6",fg=fontcolor(float("{0:.2f}".format(total_pl))),font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
    tot_pl.grid(row=coin_row,column=7,sticky=N+S+E+W)

    totcv=Label(cryptopy,text="${0:.2f}".format(totcurrentval),bg="#F3F4F6",fg="black",font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
    totcv.grid(row=coin_row,column=5,sticky=N+S+E+W)

    api=""    #for refreshing and updating

    refresh=Button(cryptopy,text="REFRESH",bg="#142E54",fg="white",command=reset,font="lato 12 ",padx="5",pady="5", borderwidth=2 ,relief="groove")
    refresh.grid(row=coin_row+1,column=7,sticky=N+S+E+W)



def app_header():
    Portfolio_id=Label(cryptopy,text="portfolio ID",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    Portfolio_id.grid(row=0,column=0,sticky=N+S+E+W)

    name=Label(cryptopy,text="coinname",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    name.grid(row=0,column=1,sticky=N+S+E+W)

    price=Label(cryptopy,text="price",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    price.grid(row=0,column=2,sticky=N+S+E+W)

    coinowned=Label(cryptopy,text="amtowned",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    coinowned.grid(row=0,column=3,sticky=N+S+E+W)

    amtpaid=Label(cryptopy,text="total_paid",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    amtpaid.grid(row=0,column=4,sticky=N+S+E+W)

    currentval=Label(cryptopy,text="current_value",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    currentval.grid(row=0,column=5,sticky=N+S+E+W)

    pl_coin=Label(cryptopy,text="p/l per coin",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    pl_coin.grid(row=0,column=6,sticky=N+S+E+W)

    tot_pl=Label(cryptopy,text="total_pl",bg="#142E54",fg="white",font="lato 12 bold",padx="5",pady="5", borderwidth=2 ,relief="groove")
    tot_pl.grid(row=0,column=7,sticky=N+S+E+W)

app_nav()
app_header()
myportfolio()
cryptopy.mainloop()
print("program completed")

cursorObj.close()
con.close()
