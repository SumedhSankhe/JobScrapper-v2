source('D:/Github/mail_function.r')


past_day <- function(dt){
  # change the datetime columns to proper type
  dt[,dttm := as.POSIXct(dttm, 'EST')]
  dt[, date := as.Date(dttm,'EST')]
  # get only the posts in the last 24 hours
  newDT <- dt[date > (Sys.Date() - 1)]
  # create a hyperlink to add to the html table
  newDT[,Title := paste0('<a href="',link,'">', Title,"</a>")]
  mailDT <-  newDT[,.(Company, Location, Title, Summary)]
  text <- paste0('Found <b>', nrow(newDT), '</b> new positions, check the table below for something new')
  
  # logic for adding an attachment to the email
  if (nrow(dt) > 20){
    tempfile <- tempfile(pattern = 'data', fileext = '.csv')
    write.csv(mailDT, tempfile)
    text <- paste0(text,'\n ', 'Showing only the first 20 posts see attachment for complete list')
    email <- list(text, head(mailDT, 20))
  }else{
    tempfile <- NULL
    email <- list(text, mailDT)
  }
  #send mail and delete the temporary file
  mail_me(email, subject = '#Automation: Daily Posts', attachments = tempfile)
  unlink(tempfile)
  return(print('Done'))
}

analysis_fornight <- function(dt){
  # TODO 15 day analysis of the job postings
  
  dt[,dttm:= as.POSIXct(dttm,'EST')]
  dt[,date:= as.Date(dttm, 'EST')]
  newDT <- dt[date > Sys.Date() - 15]
  anaDT <- newDT[,.N,Company]
  
  mail_me(list(head(anaDT[order(-N)],10)), subject = '#Automation: Fornightly Report')
  
  return(print('Done'))
}

library(data.table)
dt <-  as.data.table(read.csv("D:/Github/JobScrapper-v2/master_data/master.csv", stringsAsFactors = F))
past_day(dt)


