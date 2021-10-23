import random

def battle(characters, enemies):
    characters_temp = characters[:]
    enemies_temp = enemies[:]
    allies_died = []

    # Remove dead characters
    for char in characters:
        if char.dead:
            characters_temp.remove(char)

    # All attackers in order of speed
    all_attackers = characters_temp + enemies_temp
    all_attackers = sorted(all_attackers, key=lambda x: x.speed, reverse=True)
    # All defenders added number = to target # (Different chances to be attacked)
    ally_multi_targets = []
    for idx in range(len(characters_temp)):
        ally_multi_targets = ally_multi_targets + [characters_temp[idx] for x in range(characters_temp[idx].target)]
    enemy_multi_targets = []
    for idx in range(len(enemies_temp)):
        enemy_multi_targets = enemy_multi_targets + [enemies_temp[idx] for x in range(enemies_temp[idx].target)]
    # Attack loop until all of one group is dead.
    while characters_temp and enemies_temp:
        for attacker in all_attackers:

            # Character attacks:
            if type(attacker).__name__ == 'Character':
                #Select enemy to attack
                target_enemy = random.choice(enemy_multi_targets)

                # calculate damage
                damage = attacker.attack - (attacker.attack * target_enemy.defense)
                # Black mage attack takes MP, reduce damage once out
                if attacker.name == "Black Mage":
                    attacker.mp -= 5
                    if attacker.mp <= 0:
                        attacker.mp = 0
                        damage = 2
                target_enemy.health -= damage
                # If dead remove enemy from list
                if target_enemy.health <= 0:
                    enemies_temp.remove(target_enemy)
                    enemy_multi_targets = [n for n in enemy_multi_targets if n != target_enemy]
                # If all enemies dead, win
                if not enemies_temp:
                    break

            # Enemy Attacks:
            if type(attacker).__name__ == 'Enemies':
                #Select ally to attack
                target_ally = random.choice(ally_multi_targets)
                # calculate damage
                damage = attacker.attack - (attacker.attack * target_ally.defense)
                target_ally.health -= damage
                target_ally.damage_lost -= damage
                # If dead, remove ally from list
                if target_ally.health <= 0:
                    target_ally.health = 0
                    characters_temp.remove(target_ally)
                    ally_multi_targets = [n for n in ally_multi_targets if n != target_ally]
                    target_ally.dead = True
                    allies_died.append(target_ally.name)

                # If all characters dead, lose
                if not characters_temp:
                    break
    game_over = False
    if not characters_temp:
        game_over = True

    return allies_died, game_over


# Test: -------------------------------------------
# from characters import character_list, enemy_group, Enemies
# enemy_list = enemy_group('Group F')
# battle(character_list, enemy_list)
# enemy_list = [Enemies('Goblin King'), Enemies('Goblin King'), Enemies('Goblin King'), Enemies('Goblin King'), Enemies('Goblin King')]
# battle(character_list, enemy_list)
