class Chat:
    # knowledge that the AI has
    knowledge = {
        "what is this chapter?": "ElAl!",
        "when was ElAl established?": "2005",
        "who is our brother chapter?": "SiWi",
        "how do i join?": "Email elalmorah@gmail.com to join or come to events, don't worry coming to an event is not binding, just a fun way to meet the chapter and try out fun activities!",
        "how do i find the ElAl facebook page?": "The ElAl Twitter group can be found at @ELALBBG1863 on Twitter, and shows all elections results live!",
        "how do i find the ElAl instagram page?": "The ElAl Instagram group can be found at @elalbbg on Instagram, and shows many images from all ElAl events!",
        "how do i find the ElAl twitter page?": "The ElAl Facebook group is for members only to find events and information, but you can find it at @El Al BBG #1863 on Facebook",
    }

    def response(self, user_input):
        if user_input in self.knowledge:
            return self.knowledge[user_input]
        else:
            return "Sorry, I'm not sure how to answer that, maybe try to be more specific? Email elalbbgnsiah@gmail.com if you have any questions and for more information!"