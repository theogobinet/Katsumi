#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources import interactions as it

def asciiArt():
    it.clear()
    return print( """
                                        .      .       .       .
            .   .       .   1217   .      . .      .         .     337   .    .
                    .       .         .    .   .         .         .            .
            .   .    .       .         . . .        .  2027   .     .    .
            .     13    .   .       .       . .      .        .  .              .
                .  .    .  .       .     . .    .       . .      .   .        .
            .   .       .    . .   89 .    . .   .      .     .    109    .     .
            .            .    .     .   . .  .     .   .               .
                .               .  .    .  . . .    .  .                 .
                                . .  .  . . .  . .
                                    . . . . . .
                                        . . . .
                                        I . I
                          _______________III_______________
                         |    .   Prime   .  Numbers   .   |
                          \SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS/
                             \ ======================= /
                                  \SSSSSSSSSSSSSSSSS/
                               ________\       /________
                              (=+=+=+=+=+=+=+=+=+=+=+=+=)
                               ~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    )


def asciiJongling():
    it.clear()
    return print(
        """
                        '   '    '     
                        '   '    '   
                    o/          '  \o 
                    /-'            -\ 
                    /\               /\
                    
            Do you feel as though you are juggling 
                a few to many responsibilities?
        """
    )

def asciiDeath():
    it.clear()
    return print('''
                    %%% %%%%%%%            |#|
                %%%% %%%%%%%%%%%        |#|####
            %%%%% %         %%%       |#|=#####
            %%%%% %   @    @   %%      | | ==####
            %%%%%% % (_  ()  )  %%     | |    ===##
            %%  %%% %  \_    | %%      | |       =##
            %    %%%% %  u^uuu %%     | |         ==#
                %%%% %%%%%%%%%      | |           V
            
            ~ Death is irreversible ~
    '''
    )

def asciiKeys():
    it.clear()
    return print(
        """
        8 8          ,o.                                        ,o.          8 8
        d8o8azzzzzzzzd   b        Diffie Hellman Key           d   bzzzzzzzza8o8b
                    `o'               Exchange                  `o'

            8 8 8 8                     ,ooo.
            8a8 8a8                    oP   ?b
            d888a888zzzzzzzzzzzzzzzzzzzz8     8b
            `""^""'                    ?o___oP'
            
            """
    )

def asciiBark():
    it.clear()
    return print(
        """
    .-------------.                        .    .   *       *   
    /_/_/_/_/_/_/_/ \    certification        *   .   )    .
    //_/_/_/_/_/_// _ \ __      authority (CA)   .        .   
    /_/_/_/_/_/_/_/|/ \.' .`-o                 *    .  
    |             ||-'(/ ,--'                    
    |    Benji    ||  _ |         BARK Trust Services                      
    |             ||'' ||                        
    |_____________|| |_|L                     

        """
    )


def asciiCat():
    it.clear()
    return print('''                         
       _                        
       \`*-.                 _  __     _                       _    
        )  _`-.             | |/ /    | |                     (_)    
       .  : `. .            | ' / __ _| |_ ___ _   _ _ __ ___  _     
       : _   '  \           |  < / _` | __/ __| | | | '_ ` _ \| |    
       ; *` _.   `*-._      | . \ (_| | |_\__ \ |_| | | | | | | |    
       `-.-'          `-.   |_|\_\__,_|\__|___/\__,_|_| |_| |_|_|    
         ;       `       `.     
         :.       .        \               Remember: 
         . \  .   :   .-'   .     Encryption provides secrecy,
         '  `+.;  ;  '      :    not authentication or integrety.
         :  '  |    ;       ;-. 
         ; '   : :`-:     _.`* ;  Martin Azaël && Gobinet Théo 
     .*' /  .*' ; .*`- +'  `*' 
      `*-*   `*-*  `*-*'           
                                               
''')
